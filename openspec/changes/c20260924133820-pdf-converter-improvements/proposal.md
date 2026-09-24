## Why

A experiência do usuário com o PdfToMarkdown precisa de maior clareza visual durante inferências longas, persistência histórica das conversões realizadas e suporte nativo a múltiplos arquivos com empacotamento consolidado em ZIP, além de simplificar a seleção de arquivos na interface.

## What Changes

- **Seleção Múltipla Simplificada**: O botão "Buscar em Pasta" é removido; o botão principal passa a se chamar "Selecionar arquivos PDF", permitindo seleção única ou múltipla de PDFs (`askopenfilenames`).
- **Contador em Tempo Real**: Durante o envio de cada página para o modelo local, um cronômetro/contador de segundos decorridos atualiza dinamicamente a mensagem na interface.
- **Auto-scroll Confiável**: A área de rolagem dos logs desce automaticamente até o final a cada nova mensagem ou atualização de status.
- **Nomenclatura e ZIP**: O arquivo individual gerado receberá o sufixo `_convert.md` (`{nome_original}_convert.md`). Quando múltiplos PDFs forem convertidos, gera um arquivo `.zip` contendo todos os Markdown convertidos.
- **Histórico em SQLite**: Criação de banco de dados SQLite local (`history.db`) registrando metadados de cada conversão: nome do arquivo, caminho, data/hora de início/fim, nome do computador/host, quantidade de páginas e status.

## Capabilities

### New Capabilities
- `conversion-history`: Registro e consulta de histórico das conversões em banco SQLite local contendo arquivo, data/hora, máquina e status.

### Modified Capabilities
- `desktop-gui`: Substituição do botão por "Selecionar arquivos PDF" com suporte a múltiplos itens, inclusão de contador de segundos decorridos em tempo real na bolha de envio de página e garantia de auto-scroll para cada atualização.
- `pdf-markdown-conversion`: Salvar arquivo com sufixo `_convert.md` e gerar arquivo `.zip` consolidado quando múltiplos PDFs forem processados.

## Impact

- `src/PdfToMarkdown/app.py`: Interface ajustada para seleção múltipla, remoção do botão de pasta e gerenciamento de timer de atualização.
- `src/PdfToMarkdown/pdf_pipeline.py`: Tratamento de múltiplos arquivos, retorno de caminho único ou ZIP e nomeação com `_convert.md`.
- `src/PdfToMarkdown/Infrastructure/` (ou `history_db.py`): Módulo de acesso ao banco SQLite para gravação de histórico.
- Testes unitários atualizados e expandidos.
