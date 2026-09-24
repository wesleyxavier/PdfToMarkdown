## 0. Branch

- [x] 0.1 Criar worktree isolada (skill `openspec-worktree`): `feature/pdf-to-markdown-converter`, base na branch padrão do projeto (após `bootstrap-setup` mergeado)

## 1. Dependências e estrutura

- [x] 1.1 Adicionar `customtkinter`, `pymupdf`, `openai` ao `pyproject.toml`
- [x] 1.2 Criar módulo `src/PdfToMarkdown/app.py` (entrypoint da GUI)
- [x] 1.3 Criar módulo `src/PdfToMarkdown/llama_lifecycle.py` (start/health-check/stop do `llama-server`)
- [x] 1.4 Criar módulo `src/PdfToMarkdown/pdf_pipeline.py` (render de páginas, chamada OCR, montagem do Markdown)

## 1.1 Commit Group 1

- [x] git commit -m "feat: estrutura base e dependencias do PdfToMarkdown"
- [x] git push

## 2. Ciclo de vida do llama-server

- [x] 2.1 Implementar `start_llama_server()`: `subprocess.Popen` com `--model "C:\LLamaModels\Qwen3-VL-4B-Instruct-Q4_K_M.gguf" --port 8081` (demais flags conforme `design.md`)
- [x] 2.2 Implementar health-check com timeout em `http://localhost:8081/health`, com feedback na UI enquanto aguarda
- [x] 2.3 Implementar `stop_llama_server()` via `terminate()`/`kill()`, registrado em `atexit` e no `WM_DELETE_WINDOW` da janela principal
- [x] 2.4 Tratar erro de porta ocupada / falha ao subir o processo com mensagem clara na UI

## 2.1 Commit Group 2

- [x] git commit -m "feat: ciclo de vida do llama-server (start/health-check/stop)"
- [x] git push

## 3. Seleção de PDF e GUI

- [x] 3.1 Implementar seleção de arquivo único via `filedialog.askopenfilename` (filtro `*.pdf`)
- [x] 3.2 Implementar seleção de pasta via `filedialog.askdirectory` + listagem de PDFs encontrados
- [x] 3.3 Implementar área de log em bolhas (cores por tipo: sistema/aviso/sucesso/erro) conforme protótipo do usuário
- [x] 3.4 Implementar gate de permissão humano (`threading.Event`, botões Permitir/Recusar) antes do envio de páginas

## 3.1 Commit Group 3

- [x] git commit -m "feat: selecao de PDF e interface grafica (customtkinter)"
- [x] git push

## 4. Pipeline de conversão

- [x] 4.1 Implementar render de página em imagem (PyMuPDF, 150 DPI) + encode base64
- [x] 4.2 Implementar chamada ao endpoint de chat completions (`base_url=http://localhost:8081/v1`) solicitando transcrição em Markdown
- [x] 4.3 Tratar falha de página individual (erro de rede/timeout) interrompendo o restante do pipeline com mensagem clara
- [x] 4.4 Montar e salvar o Markdown final (`resultado.md` ou nome derivado do PDF de entrada), exibindo caminho absoluto ao concluir
- [x] 4.5 Executar todo o pipeline em thread separada da UI (worker thread `daemon=True`)

## 4.1 Commit Group 4

- [x] git commit -m "feat: pipeline de conversao PDF para markdown via OCR visual local"
- [x] git push

## 5. Testes

- [x] 5.1 Teste unitário do parsing/montagem do Markdown final (mock da resposta do modelo)
- [x] 5.2 Teste unitário do health-check do llama-server (mock de `requests`)
- [x] 5.3 Rodar app real (skill `run`) com um PDF de teste e um `llama-server` já validado, confirmar geração do `.md` ponta a ponta

## 6. Pre-PR Checklist

- [x] 6.1 Atualizar README.md com instruções de uso (como rodar, requisito do modelo em `C:\LLamaModels\`, dependência do `llama-server.exe`)
- [x] 6.2 Rodar `graphify update .`

## 7. Create PR

- [x] 7.1 Commit final + push
- [x] 7.2 Criar PR (`feature/pdf-to-markdown-converter` → branch padrão do projeto)
