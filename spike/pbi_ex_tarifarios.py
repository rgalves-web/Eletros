#!/usr/bin/env python3
"""Spike descartável: extrai as tabelas do painel Power BI público de
consultas públicas de ex-tarifários (SDIC/MDIC).

Duas etapas, ambas sem login:

  1. capture  -> abre o relatório num Chromium sem interface (Playwright),
                 percorre as páginas do relatório e grava cada POST
                 /public/reports/querydata (pedido + resposta) e as respostas
                 de modelsAndExploration / conceptualschema em OUTDIR/raw/.
  2. replay   -> reenvia por HTTP puro cada consulta capturada que tenha forma
                 de tabela (DataReduction com Window), paginando por
                 RestartTokens, decodifica o formato DSR e grava um CSV por
                 visual em OUTDIR/tables/.

Uso:
  pip install playwright && playwright install chromium     # se preciso
  python3 pbi_ex_tarifarios.py capture  --out saida
  python3 pbi_ex_tarifarios.py replay   --out saida
  python3 pbi_ex_tarifarios.py all      --out saida         # as duas

Só usa a biblioteca padrão + playwright. Escrito do zero para este spike
(o projeto cameronaaron/powerbi-extract, AGPL-3.0, foi lido como referência
do protocolo, mas nenhum código foi copiado).
"""

import argparse
import base64
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

VIEW_URL = (
    "https://app.powerbi.com/view?r=eyJrIjoiMzM3ZmNhOTAtZDZmOC00OGYzLWJjZmYtNzNl"
    "NWU5NWFiYzZmIiwidCI6IjQ1NjIxM2NmLTcwNzMtNDdjNi1iZjQ5LTQxYjY1NGFkNDQ5YiJ9"
)
QUERYDATA = "/public/reports/querydata"
INTERESTING = ("querydata", "modelsAndExploration", "conceptualschema")


def resource_key(view_url):
    r = view_url.split("r=", 1)[1].split("&", 1)[0]
    r += "=" * (-len(r) % 4)
    return json.loads(base64.b64decode(r))["k"]


# --------------------------------------------------------------------------
# 1. captura com navegador sem interface
# --------------------------------------------------------------------------
def capture(view_url, out, wait_s):
    from playwright.sync_api import sync_playwright, Error as PwError

    raw = out / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    counter = {"n": 0}

    def on_response(resp):
        url = resp.url
        if not any(k in url for k in INTERESTING):
            return
        counter["n"] += 1
        n = counter["n"]
        req = resp.request
        try:
            body = resp.body()
        except PwError:
            body = b""
        rec = {
            "url": url,
            "method": req.method,
            "status": resp.status,
            "request_headers": {k: v for k, v in req.headers.items()
                                if k.lower().startswith(("x-powerbi", "activityid",
                                                         "requestid", "content-type"))},
            "request_body": req.post_data,
        }
        (raw / f"{n:03d}.meta.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1))
        (raw / f"{n:03d}.body.json").write_bytes(body)
        print(f"[capture] {n:03d} {resp.status} {url.split('?')[0]}")

    launch = {}
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if proxy:  # usa o proxy oficial do ambiente, quando existir
        launch["proxy"] = {"server": proxy}

    with sync_playwright() as p:
        browser = p.chromium.launch(**launch)
        page = browser.new_page(viewport={"width": 1600, "height": 1000})
        page.on("response", on_response)
        page.goto(view_url, wait_until="networkidle", timeout=120_000)
        page.wait_for_timeout(wait_s * 1000)
        # rola as tabelas para forçar a carga de mais janelas de linhas
        for _ in range(6):
            page.mouse.wheel(0, 2000)
            page.wait_for_timeout(1500)
        # percorre as páginas do relatório (botão "Próxima página"/"Next Page")
        for _ in range(15):
            btn = page.query_selector("button[aria-label*='Next'], button[aria-label*='Próxima']")
            if not btn:
                break
            try:
                btn.click(timeout=3000)
            except PwError:
                break
            page.wait_for_timeout(wait_s * 1000)
        page.screenshot(path=str(out / "painel.png"), full_page=True)
        browser.close()
    print(f"[capture] {counter['n']} respostas gravadas em {raw}")


# --------------------------------------------------------------------------
# 2. reenvio por HTTP e decodificação DSR
# --------------------------------------------------------------------------
def decode_dsr(resp_json):
    """Converte uma resposta querydata em (colunas, linhas, restart_tokens)."""
    try:
        data = resp_json["results"][0]["result"]["data"]
        ds = data["dsr"]["DS"][0]
    except (KeyError, IndexError, TypeError):
        return [], [], None
    names = {}
    for sel in data.get("descriptor", {}).get("Select", []) or []:
        if sel and sel.get("Value"):
            names[sel["Value"]] = sel.get("Name", sel["Value"])
    dicts = ds.get("ValueDicts", {})
    rows, schema, prev = [], [], []
    cols = []
    for ph in ds.get("PH", []):
        for ent in ph.get("DM0", []):
            if "S" in ent:
                schema = ent["S"]
                cols = [names.get(f["N"], f["N"]) for f in schema]
                prev = [None] * len(schema)
            if not schema or "C" not in ent and "R" not in ent and "Ø" not in ent:
                continue
            vals = iter(ent.get("C", []))
            rmask, nmask = ent.get("R", 0), ent.get("Ø", 0)
            row = []
            for i, f in enumerate(schema):
                if rmask >> i & 1:
                    v = prev[i]
                elif nmask >> i & 1:
                    v = None
                else:
                    v = next(vals, None)
                    dn = f.get("DN")
                    if dn and isinstance(v, int) and not isinstance(v, bool) and dn in dicts:
                        v = dicts[dn][v]
                row.append(v)
            prev = row
            rows.append(row)
    return cols, rows, ds.get("RT")


def post(url, headers, payload, retries=4):
    data = json.dumps(payload).encode()
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=data, method="POST", headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (401, 403, 429, 500, 502, 503, 504) and attempt < retries:
                time.sleep(2 ** attempt)
                continue
            raise


def replay(out, page_size):
    raw = out / "raw"
    tables = out / "tables"
    tables.mkdir(parents=True, exist_ok=True)
    seen = set()
    for meta_path in sorted(raw.glob("*.meta.json")):
        meta = json.loads(meta_path.read_text())
        if QUERYDATA not in meta["url"] or not meta.get("request_body"):
            continue
        body = json.loads(meta["request_body"])
        q = body["queries"][0]
        cmd = q["Query"]["Commands"][0]["SemanticQueryDataShapeCommand"]
        key = json.dumps(cmd["Query"], sort_keys=True)
        if key in seen:
            continue
        seen.add(key)
        primary = ((cmd.get("Binding") or {}).get("DataReduction") or {}).get("Primary") or {}
        if "Window" not in primary:
            continue  # cartões/KPIs/segmentações: ignorados neste spike
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Origin": "https://app.powerbi.com",
            "Referer": "https://app.powerbi.com/",
            "X-PowerBI-ResourceKey": meta["request_headers"].get(
                "x-powerbi-resourcekey", resource_key(VIEW_URL)),
        }
        all_rows, cols, rt, page = [], [], None, 0
        while True:
            page += 1
            window = {"Count": page_size}
            if rt:
                window["RestartTokens"] = rt
            cmd["Binding"]["DataReduction"]["Primary"] = {"Window": window}
            payload = dict(body)
            payload["queries"] = [q]
            resp = post(meta["url"], headers, payload)
            c, rows, rt = decode_dsr(resp)
            cols = cols or c
            if all_rows and rows and rows[0] == all_rows[-1]:
                rows = rows[1:]
            all_rows.extend(rows)
            print(f"[replay] {meta_path.stem} pág {page}: +{len(rows)} (total {len(all_rows)})")
            if not rt or not rows:
                break
        dest = tables / f"{meta_path.stem.split('.')[0]}.csv"
        with dest.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(cols)
            w.writerows(all_rows)
        print(f"[replay] {len(all_rows)} linhas, colunas {cols} -> {dest}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["capture", "replay", "all"])
    ap.add_argument("--out", default="saida_pbi")
    ap.add_argument("--url", default=VIEW_URL)
    ap.add_argument("--wait", type=int, default=10, help="segundos de espera por página")
    ap.add_argument("--page-size", type=int, default=500)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if a.step in ("capture", "all"):
        capture(a.url, out, a.wait)
    if a.step in ("replay", "all"):
        replay(out, a.page_size)


if __name__ == "__main__":
    sys.exit(main())
