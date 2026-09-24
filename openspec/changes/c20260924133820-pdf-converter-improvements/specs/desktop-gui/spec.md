## MODIFIED Requirements

### Requirement: Seleção do PDF de entrada
O sistema SHALL permitir ao usuário selecionar um ou múltiplos arquivos PDF de entrada via diálogo nativo do Windows através do botão "Selecionar arquivos PDF", sem botão separado para pastas.

#### Scenario: Seleção de múltiplos arquivos PDF
- **WHEN** usuário clica em "Selecionar arquivos PDF"
- **THEN** o sistema abre o diálogo nativo do Windows filtrado por `*.pdf` permitindo seleção múltipla (`askopenfilenames`) e exibe a contagem de arquivos selecionados

### Requirement: Log de execução em bolhas
O sistema SHALL exibir cada etapa relevante do pipeline como uma bolha de mensagem na área de log, com cores distintas por tipo (sistema, aviso, sucesso, erro), exibindo contador de segundos decorridos em tempo real durante o envio de cada página e garantindo a descida automática do scroll (auto-scroll) a cada nova mensagem ou atualização.

#### Scenario: Envio de página com contador dinâmico
- **WHEN** uma página está sendo processada pelo modelo local
- **THEN** o sistema exibe e atualiza a cada segundo uma contagem do tempo decorrido na respectiva bolha (ex: `(12s)`)

#### Scenario: Auto-scroll garantido
- **WHEN** qualquer nova bolha for adicionada ou tiver seu texto atualizado
- **THEN** o sistema atualiza a visualização e rola o scroll até a extremidade inferior
