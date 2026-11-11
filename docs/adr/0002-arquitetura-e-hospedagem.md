# ADR-0002: Monólito Python num servidor virtual próprio, com agente via Agent SDK

**Data**: 2026-11-11
**Status**: aceito
**Decidido em**: [Entrevista: arquitetura e hospedagem](https://github.com/rgalves-web/eletros/issues/10)

## Contexto

O sistema reúne coleta agendada (INLABS, páginas e PDFs da Camex, painel Power BI via Playwright), um agente que lê atos e propõe cadastros com apoio do cérebro em git (ADR-0001), um banco relacional derivado, dashboard com conversa com o agente, editor web do cérebro e envio de e-mails. A aplicação é própria, administrada por um único responsável, sem restrição de plataforma imposta pela TI da Eletros. Faltava escolher onde hospedar e com que peças montar.

## Decisão

- **Hospedagem**: um servidor virtual na Hetzner, com disco criptografado, rodando tudo via Docker Compose (web, worker, Postgres, Caddy). Cópia diária do dump do Postgres e dos arquivos (ZIPs do INLABS, PDFs, documentos restritos) para um bucket S3-compatível. Clone do cérebro no disco do servidor, com o GitHub (`eletros-cerebro`, privado) como remoto.
- **Aplicação**: monólito em Python com Django e HTMX, numa única base de código para coletores, agente, interface e e-mail. Postgres com pgvector como índice derivado e como busca semântica usada pelo agente como ferramenta.
- **Agente**: Claude Agent SDK (Python), com o clone do cérebro como diretório de trabalho, escrita permitida só em `propostas/`, `fontes/` e sínteses, e ferramentas próprias (regex de NCM, busca lexical, consulta ao índice). O mesmo runtime atende à leitura de atos e à conversa no dashboard. Modelos por tarefa em configuração: Sonnet para leitura e proposição, Opus para sínteses e lint semanal, Haiku para a triagem dos órgãos fora da lista-chave.
- **Agendamento**: um worker com APScheduler e tabela de jobs no Postgres, sem Redis nem Celery.
- **Identidade e e-mail**: login pela conta Microsoft de cada usuário (Entra ID, OIDC) restrito ao tenant da Eletros; envio pela caixa institucional `cacex@eletros.org.br` via Microsoft Graph (`Mail.Send` limitado a essa caixa), ambos numa única aplicação registrada no Entra. Se o registro da aplicação depender da TI e atrasar, senha própria com TOTP como alternativa provisória.
- **Domínio**: domínio independente da Eletros no início, com DNS na Cloudflare e certificado automático pelo Caddy; um subdomínio da Eletros pode apontar para o mesmo servidor depois.
- **Implantação e operação**: GitHub Actions com SSH sobe a nova imagem a cada push na `main`; sem ambiente de homologação na v1. Segredos num `.env` só no servidor. Cada coleta registra resultado na página da fonte monitorada e no banco; e-mail ao administrador após duas falhas seguidas da mesma fonte ou erro do agente; Sentry para erros da aplicação.

## Alternativas rejeitadas

- **Plataforma gerenciada (Railway, Fly.io, Render)**: menos administração, porém o clone git persistente, o Chromium do Playwright e o volume de ZIPs e documentos encaixam mal e encarecem; para um administrador único que já usa terminal, o servidor virtual custa menos e dá controle total.
- **Serverless**: incompatível com jobs de minutos do agente e com o clone git no disco.
- **Backend Python e interface em TypeScript**: duas linguagens para manter sem ganho para telas de filtro, ficha de processo e chat, que HTMX com SSE atende.
- **Loop próprio sobre a Messages API**: repete o que o Agent SDK já faz (sistema de arquivos como contexto, permissões por pasta, ferramentas), que é exatamente o padrão de leitura "ato + índice + esquema + páginas indicadas" do cérebro.
- **Celery com Redis**: robustez desnecessária para dezenas de atos por dia; a tabela de jobs em Postgres já dá reexecução e auditoria.
- **Provedor de e-mail transacional**: exigiria domínio verificado e contrato; a caixa institucional entrega sem cair em spam e sem custo.
- **Servidor em provedor brasileiro**: duas a três vezes o custo pelo mesmo porte; os documentos guardados são de processos administrativos públicos ou de autos restritos sem dados pessoais sensíveis, o que torna a guarda fora do Brasil defensável.

## Consequências

- A conversa com o agente no dashboard (por processo e geral) usa o mesmo runtime e as mesmas regras de escrita: pode criar propostas, nunca aplica em página definitiva; histórico de conversa fica no banco, fora do cérebro.
- O registro da aplicação no Entra (login e `Mail.Send`) é tarefa humana que precisa do domínio escolhido para as URLs de retorno.
- O servidor precisa de Chromium para o Playwright e de espaço de disco crescente para ZIPs e documentos; o bucket é o destino de longo prazo.
- Um custo mensal previsível (servidor, bucket, Cloudflare, uso de LLM, Sentry) pode ser estimado antes da construção.
