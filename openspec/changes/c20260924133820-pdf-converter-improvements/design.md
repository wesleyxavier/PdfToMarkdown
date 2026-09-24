## Context

O aplicativo desktop PdfToMarkdown converte PDFs para Markdown via LLM multimodal local. O fluxo atual foi validado, mas requer melhorias de produtividade e rastreabilidade:
1. Suporte a seleção de múltiplos arquivos PDF de uma só vez (substituindo a opção de busca em pasta por multi-seleção nativa).
2. Cronômetro dinâmico em segundos visível durante o envio de cada página para o modelo local.
3. Banco de dados SQLite local (`history.db`) para rastrear o histórico de cada conversão (arquivo, máquina, data/hora, páginas, status).
4. Padrão de nomenclatura `{nome}_convert.md` e empacotamento automático em arquivo `.zip` quando múltiplos PDFs forem convertidos.
5. Garantia de auto-scroll suave na área de chat em qualquer nova mensagem ou atualização de status.

## Goals / Non-Goals

**Goals:**
- Permitir ao usuário selecionar 1 ou N arquivos PDF usando o diálogo nativo do Windows (`askopenfilenames`).
- Exibir contagem de tempo em segundos correndo na bolha de status durante o envio de cada página (ex: `Enviando página 1/6 para o modelo local... (14s)`).
- Persistir histórico completo em SQLite (`history.db`), sem dependências externas adicionais (usando biblioteca padrão `sqlite3`).
- Salvar arquivos com sufixo `_convert.md`. Quando houver 2 ou mais PDFs, empacotar todos em um único arquivo `.zip` no diretório dos arquivos.
- Garantir rolagem automática até o final do scroll a cada nova bolha ou atualização de timer.

**Non-Goals:**
- Não adicionar interface complexa de consulta SQL na GUI nesta change (o foco é a gravação estruturada no banco).
- Não alterar a porta ou parâmetros base do `llama-server`.

## Decisions

1. **Persistência SQLite com `sqlite3`**:
   - Criação do módulo `src/PdfToMarkdown/Infrastructure/history_db.py`.
   - Banco criado automaticamente em `history.db` (na raiz do projeto ou diretório da aplicação).
   - Tabela `conversions`:
     - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
     - `filename` (TEXT)
     - `file_path` (TEXT)
     - `output_path` (TEXT)
     - `page_count` (INTEGER)
     - `computer_name` (TEXT - obtido via `platform.node()` ou `os.environ['COMPUTERNAME']`)
     - `started_at` (TEXT ISO8601)
     - `finished_at` (TEXT ISO8601)
     - `duration_seconds` (REAL)
     - `status` (TEXT: 'SUCCESS', 'FAILED', 'CANCELLED')
     - `error_message` (TEXT NULL)

2. **Cronômetro Dinâmico por Página**:
   - Durante a chamada `ocr_page_image`, uma thread secundária de timer (ou polling com intervalo de 1s) atualiza o texto da bolha ativa da página com `(Xs)`.
   - Ao concluir a página, a bolha finaliza com o status de sucesso e tempo total gasto.

3. **Substituição de Botões e Nomenclatura**:
   - Remoção do botão "Buscar em Pasta" da interface.
   - Botão renomeado para "Selecionar arquivos PDF" com `filedialog.askopenfilenames(...)`.
   - Nomenclatura do arquivo gerado: `{path.stem}_convert.md`.
   - Quando múltiplos arquivos forem selecionados, o pipeline itera sobre todos e gera um `.zip` com `zipfile.ZipFile` reunindo todos os arquivos `_convert.md`.

4. **Auto-Scroll no CustomTkinter**:
   - Usar `self.chat_frame.update_idletasks()` seguido de `self.chat_frame._parent_canvas.yview_moveto(1.0)` dentro de `self.after(20, ...)` para garantir que o Canvas recalcule sua altura antes do movimento de rolagem.

## Risks / Trade-offs

- [Múltiplos arquivos grandes podem demorar] → A interface exibe o progresso de arquivo N de M e página X de Y, com histórico gravado individualmente no SQLite mesmo se houver falha em um arquivo posterior.
- [Concorrência no SQLite] → Gravação pontual ao início e fim de cada documento em transações rápidas; não há concorrência significativa em app desktop monoposto.
