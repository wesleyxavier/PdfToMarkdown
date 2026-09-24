# PdfToMarkdown

App desktop Windows que converte PDF em Markdown usando OCR visual via LLM multimodal local (`llama.cpp`), sem depender de serviço cloud.

## O que é

Interface gráfica (`customtkinter`, tema escuro estilo chat) que:

1. Permite ao usuário escolher o PDF de entrada (arquivo único ou busca dentro de uma pasta) via diálogo nativo do Windows.
2. Sobe automaticamente um `llama-server` local com o modelo `Qwen3-VL-4B-Instruct-Q4_K_M.gguf` na porta `8081`.
3. Pede confirmação humana (gate de permissão com botões Permitir / Abortar) antes de iniciar o envio das páginas para o modelo.
4. Renderiza cada página do PDF como imagem (150 DPI) e envia pro modelo multimodal, solicitando transcrição fiel em Markdown com títulos, tabelas e listas.
5. Salva o Markdown final consolidado e encerra o `llama-server` automaticamente ao fechar o app.

Todo o processamento roda em thread separada da UI — a janela nunca trava durante a conversão.

## Requisitos

- **Sistema Operacional**: Windows.
- **Python**: 3.12+.
- **llama-server.exe**: instalado localmente no PATH do sistema.
- **Modelo Multimodal**: arquivo `Qwen3-VL-4B-Instruct-Q4_K_M.gguf` localizado em `C:\LLamaModels\`.

## Como Executar a Aplicação

```bash
# Ativar o ambiente virtual
.venv\Scripts\activate

# Iniciar o aplicativo desktop
python -m PdfToMarkdown
```

## Desenvolvimento e Testes

### 1. Instalar dependências
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

### 2. Executar Linter
```bash
ruff check .
```

### 3. Executar Testes Unitários e Cobertura
```bash
pytest --cov=src/PdfToMarkdown --cov-report=term-missing
```

### 4. Build e Execução via Docker
```bash
# Build da imagem multi-stage
docker build -t pdftomarkdown:latest .

# Teste de execução no container
docker run --rm pdftomarkdown:latest
```

## Arquitetura

O projeto adota Clean Architecture de 4 camadas:
- **`Domain/`**: Entidades e regras de domínio.
- **`Application/`**: Orquestração e pipeline de conversão de PDFs (`pdf_pipeline.py`).
- **`Infrastructure/`**: Gerenciamento de processos locais e subprocessos do servidor de IA (`llama_lifecycle.py`).
- **`Api/`**: Camada de apresentação e interface desktop CustomTkinter (`app.py`).
