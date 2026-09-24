## Why

Conversão de PDF pra Markdown hoje exige extração manual ou serviços cloud pagos. App desktop com OCR visual via LLM local (llama.cpp) resolve offline, sem custo de API, com controle humano em cada etapa do processo.

## What Changes

- Novo app desktop Python (`customtkinter`) com interface estilo chat escuro, log de execução em bolhas coloridas por tipo (sistema/aviso/sucesso/erro).
- Seleção de PDF via diálogo nativo do Windows (arquivo único ou busca em pasta) — sem caminho fixo hardcoded.
- Pipeline de conversão: renderiza cada página do PDF em imagem (PyMuPDF), envia pra modelo multimodal local via API OpenAI-compatible, monta Markdown final com marcador de página.
- Gate de permissão humano: app pausa (via `threading.Event`) antes de iniciar o envio de páginas pro modelo, aguardando clique em "Permitir"/"Recusar".
- Gerenciamento do ciclo de vida do `llama-server`: sobe automaticamente com modelo `Qwen3-VL-4B-Instruct-Q4_K_M.gguf` na porta `8081` ao iniciar o app, encerra o processo do server ao fechar o app.

## Capabilities

### New Capabilities
- `pdf-markdown-conversion`: pipeline de extração página-a-página do PDF (render → OCR visual via LLM local → montagem do Markdown final).
- `desktop-gui`: interface gráfica desktop (customtkinter) com log em bolhas, seleção de PDF via diálogo nativo, e gate de permissão humano antes de etapas custosas.
- `llama-server-lifecycle`: sobe `llama-server` com modelo e porta fixos junto do app, garante encerramento do processo ao fechar o app (inclusive em crash/exceção).

## Impact

- Novo projeto Python (`src/PROJETOS/PdfToMarkdown`), sem impacto em outros projetos do workspace.
- Depende de `llama-server.exe` instalado localmente (ver skill `llama-local-ai`) e do arquivo de modelo `Qwen3-VL-4B-Instruct-Q4_K_M.gguf` em `C:\LLamaModels\`.
- Dependências novas: `customtkinter`, `pymupdf`, `openai` (client SDK, usado apenas como wrapper HTTP pro endpoint OpenAI-compatible do llama.cpp).
