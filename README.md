# PdfToMarkdown

App desktop Windows que converte PDF em Markdown usando OCR visual via LLM multimodal local (`llama.cpp`), sem depender de serviço cloud.

## O que é

Interface gráfica (`customtkinter`, tema escuro estilo chat) que:

1. Deixa o usuário escolher o PDF de entrada (arquivo único ou busca dentro de uma pasta), via diálogo nativo do Windows.
2. Sobe automaticamente um `llama-server` local com o modelo `Qwen3-VL-4B-Instruct-Q4_K_M.gguf` na porta `8081`.
3. Pede confirmação do usuário (gate de permissão) antes de começar o envio das páginas pro modelo.
4. Renderiza cada página do PDF como imagem e envia pro modelo, pedindo transcrição em Markdown preservando formatação (títulos, tabelas, listas).
5. Salva o Markdown final consolidado e encerra o `llama-server` automaticamente ao fechar o app.

Todo o processamento roda em thread separada — a janela nunca trava durante a conversão.

## Requisitos

- Windows.
- Python 3.12+.
- `llama-server.exe` instalado localmente — ver skill `llama-local-ai` do harness pra setup.
- Modelo `Qwen3-VL-4B-Instruct-Q4_K_M.gguf` disponível em `C:\LLamaModels\`.

## Desenvolvimento (Setup, Testes e Docker)

### 1. Criar ambiente virtual e instalar dependências
```bash
python -m venv .venv
.venv\Scripts\activate  # No Windows
pip install -e ".[dev]"
```

### 2. Executar Linter
```bash
ruff check .
```

### 3. Executar Testes
```bash
pytest
```

### 4. Build e Execução via Docker
```bash
# Build da imagem multi-stage
docker build -t pdftomarkdown:latest .

# Teste de execução no container
docker run --rm pdftomarkdown:latest
```

## Como será construído

Implementação segue a change OpenSpec `openspec/changes/c20260924105248-pdf-to-markdown-converter/` (proposal, design, specs, tasks). Resumo das decisões técnicas em `design.md`:

- **GUI**: `customtkinter`, sem servidor web.
- **PDF → imagem**: `PyMuPDF` (`fitz`), 150 DPI.
- **OCR visual**: chamada ao endpoint OpenAI-compatible do `llama-server` local (SDK `openai` como client HTTP).
- **Ciclo de vida do `llama-server`**: subido via `subprocess.Popen` pelo próprio app, encerrado via `atexit` + `WM_DELETE_WINDOW`.

## Status

Scaffold do projeto configurado (`bootstrap-setup` — pyproject, estrutura em 4 camadas, pytest, Docker, CI).
