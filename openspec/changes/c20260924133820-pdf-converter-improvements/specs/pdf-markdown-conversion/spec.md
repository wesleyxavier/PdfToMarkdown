## MODIFIED Requirements

### Requirement: Montagem do Markdown final
Após processar as páginas com sucesso, o sistema SHALL concatenar o Markdown de cada página (com separador entre páginas) e salvar em disco com o nome do arquivo original acrescido do sufixo `_convert.md`. Caso múltiplos arquivos PDF sejam convertidos, o sistema SHALL adicionalmente empacotar todos os arquivos Markdown resultantes em um arquivo compactado `.zip`.

#### Scenario: Arquivo único convertido
- **WHEN** um único arquivo PDF é processado com sucesso
- **THEN** o sistema salva o Markdown como `{nome_original}_convert.md` na mesma pasta de origem e exibe o caminho absoluto

#### Scenario: Múltiplos arquivos convertidos e empacotados em ZIP
- **WHEN** múltiplos arquivos PDF são processados em lote com sucesso
- **THEN** o sistema gera cada `{nome_original}_convert.md` e cria um arquivo `.zip` contendo todos os Markdown convertidos, exibindo o caminho absoluto do arquivo compactado
