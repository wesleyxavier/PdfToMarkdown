## ADDED Requirements

### Requirement: Seleção do PDF de entrada
O sistema SHALL permitir ao usuário selecionar o PDF de entrada via diálogo nativo do Windows, sem caminho fixo hardcoded no código.

#### Scenario: Seleção de arquivo único
- **WHEN** usuário clica em "Selecionar PDF"
- **THEN** sistema abre diálogo nativo filtrado por `*.pdf` e usa o arquivo escolhido como entrada

#### Scenario: Busca por pasta
- **WHEN** usuário opta por selecionar uma pasta em vez de um arquivo
- **THEN** sistema abre diálogo nativo de seleção de pasta e lista os PDFs encontrados nela pro usuário escolher um

### Requirement: Log de execução em bolhas
O sistema SHALL exibir cada etapa relevante do pipeline (carregamento, envio de página, sucesso, erro) como uma bolha de mensagem na área de log, com cor distinta por tipo (sistema, aviso, sucesso, erro).

#### Scenario: Nova mensagem durante o pipeline
- **WHEN** o pipeline de conversão emite uma nova mensagem de status
- **THEN** sistema adiciona uma bolha na área de log com a cor correspondente ao tipo da mensagem e rola a view até o final

### Requirement: Gate de permissão humano
O sistema SHALL pausar a execução do pipeline antes de iniciar o envio de páginas pro modelo, exibindo os botões "Permitir e Continuar" e "Recusar/Abortar", e só prosseguir após um clique do usuário.

#### Scenario: Usuário autoriza
- **WHEN** usuário clica em "Permitir e Continuar"
- **THEN** sistema libera a thread de processamento e inicia o envio das páginas

#### Scenario: Usuário recusa
- **WHEN** usuário clica em "Recusar/Abortar"
- **THEN** sistema cancela o pipeline, exibe mensagem de cancelamento e não envia nenhuma página pro modelo

### Requirement: UI não bloqueante
O sistema SHALL executar o pipeline de conversão em uma thread separada da thread principal da UI, garantindo que a janela permaneça responsiva durante todo o processamento.

#### Scenario: Processamento de PDF longo
- **WHEN** o pipeline está processando um PDF com muitas páginas
- **THEN** a janela da aplicação continua respondendo a interações do usuário (mover, redimensionar, fechar) sem travar
