## Context

Scaffold Python (`genova new`) já criado com estrutura padrão (pyproject, testes, Docker, CI cobertos na change `bootstrap-setup`). Esta change cobre a aplicação em si: um app desktop de conversão PDF→Markdown usando um modelo multimodal local via `llama.cpp` (OCR visual, sem cloud). Referência de implementação fornecida pelo usuário (código colado no pedido) usa `customtkinter` + `PyMuPDF` + client `openai` apontando pro endpoint OpenAI-compatible do `llama-server`.

## Goals / Non-Goals

**Goals:**
- App desktop único (`python -m pdf_to_markdown` ou script), roda em Windows, sem servidor web/portas expostas além do `llama-server` local.
- Seleção do PDF de entrada via diálogo nativo (arquivo ou pasta), nunca caminho hardcoded.
- `llama-server` sobe automaticamente com o app (modelo `Qwen3-VL-4B-Instruct-Q4_K_M.gguf`, porta `8081`) e é encerrado quando o app fecha — inclusive em fechamento anormal (crash, Ctrl+C, exceção não tratada).
- Pipeline não trava a UI: conversão roda em thread separada, gate de permissão humano antes do envio das páginas.

**Non-Goals:**
- Não cobre OCR de outros formatos (imagens soltas, DOCX, etc) — só PDF.
- Não cobre distribuição/empacotamento (installer, .exe standalone) — só execução via `python`.
- Não cobre fila de múltiplos PDFs em lote nesta primeira versão — um PDF por execução.

## Decisions

- **GUI: `customtkinter`** (não Tkinter puro, não web) — decisão do usuário, replica exatamente o protótipo fornecido (dark mode, bolhas de chat, botões de permissão).
- **Ciclo de vida do `llama-server` gerenciado pelo próprio app Python**, via `subprocess.Popen` (não `Start-Process` do PowerShell como na skill `llama-local-ai`, que é pensada pra uso manual/terminal) — o app precisa do handle do processo pra poder matá-lo no `atexit`/fechamento da janela. Comando:
  ```
  llama-server --model "C:\LLamaModels\Qwen3-VL-4B-Instruct-Q4_K_M.gguf" --port 8081 --embedding -b 2048 -c 32768 -np 1 --tools all -fa on -ctk q4_0 -ctv q4_0 --parallel 1
  ```
- **Encerramento garantido do subprocesso**: registrar `atexit.register` + handler `WM_DELETE_WINDOW` (`protocol("WM_DELETE_WINDOW", ...)`) chamando `process.terminate()`/`process.kill()` — cobre fechamento normal da janela e saída do interpretador. Crash do processo Python (kill -9 externo) não é coberto — aceito como risco (ver abaixo).
- **Seleção de arquivo**: `tkinter.filedialog.askopenfilename` (arquivo único, filtro `*.pdf`) como fluxo principal; `askdirectory` como alternativa pra busca dentro de uma pasta — decisão do usuário ("pasta selecionável, ou mesmo procurado o arquivo").
- **Client de inferência**: SDK `openai` apontando `base_url="http://localhost:8081/v1"` — reutiliza o protótipo já validado pelo usuário, evita reimplementar client HTTP.
- **Health-check antes do pipeline**: app faz polling em `http://localhost:8081/health` (com timeout) após subir o `llama-server`, só libera o gate de permissão quando o server responde — evita erro de conexão na primeira chamada (modelo grande demora pra carregar).

## Risks / Trade-offs

- [Modelo demora pra carregar na VRAM/RAM (Qwen3-VL-4B)] → health-check com timeout configurável + feedback visual "carregando modelo..." na UI antes de liberar o gate.
- [Processo `llama-server` órfão se o app for morto via Task Manager / kill -9] → documentar no README como matar manualmente (`taskkill /F /IM llama-server.exe`); fora do escopo cobrir kill forçado externo.
- [Porta 8081 já em uso por outro processo] → falha ao subir `llama-server` deve aparecer como mensagem de erro clara na UI, não travar silenciosamente.
- [PDF grande / muitas páginas → muitas chamadas sequenciais ao modelo, processo lento] → aceito nesta versão (non-goal: paralelismo/batch); log por página dá visibilidade de progresso.

## Migration Plan

N/A — projeto novo, sem estado anterior a migrar.

## Open Questions

- Caminho fixo `C:\LLamaModels\` pro `.gguf` — confirmar que o arquivo `Qwen3-VL-4B-Instruct-Q4_K_M.gguf` já está baixado nesse local antes de rodar a implementação.
