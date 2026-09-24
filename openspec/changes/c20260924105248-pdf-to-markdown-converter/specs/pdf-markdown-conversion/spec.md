## ADDED Requirements

### Requirement: Renderização de páginas do PDF
O sistema SHALL renderizar cada página do PDF selecionado como imagem (PNG, 150 DPI) usando PyMuPDF, na ordem sequencial do documento.

#### Scenario: PDF com múltiplas páginas
- **WHEN** usuário autoriza o início da conversão de um PDF com N páginas
- **THEN** sistema renderiza e processa as N páginas em sequência, uma por vez

### Requirement: OCR visual via modelo local
Pra cada página renderizada, o sistema SHALL enviar a imagem codificada em base64 pro endpoint de chat completions do `llama-server` local, solicitando transcrição em Markdown preservando formatação (títulos, tabelas, listas).

#### Scenario: Página processada com sucesso
- **WHEN** o modelo local retorna uma resposta válida pra uma página
- **THEN** sistema armazena o Markdown retornado, prefixado com comentário indicando o número da página

#### Scenario: Falha na chamada ao modelo
- **WHEN** a chamada ao `llama-server` falha (erro de rede, timeout, resposta inválida) pra uma página
- **THEN** sistema exibe mensagem de erro identificando a página e interrompe o processamento das páginas restantes

### Requirement: Montagem do Markdown final
Após processar todas as páginas com sucesso, o sistema SHALL concatenar o Markdown de cada página (com separador entre páginas) e salvar em um único arquivo `.md`.

#### Scenario: Conversão concluída
- **WHEN** todas as páginas do PDF foram processadas com sucesso
- **THEN** sistema grava o arquivo Markdown final no disco e informa o caminho absoluto do arquivo gerado
