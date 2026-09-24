## ADDED Requirements

### Requirement: Inicialização automática do llama-server
Ao iniciar o app, o sistema SHALL subir o processo `llama-server` com o modelo `Qwen3-VL-4B-Instruct-Q4_K_M.gguf` na porta `8081`, sem exigir que o usuário rode o comando manualmente.

#### Scenario: App iniciado com sucesso
- **WHEN** usuário abre o app
- **THEN** sistema inicia o processo `llama-server` com modelo e porta configurados e guarda o handle do processo pra gerenciamento posterior

### Requirement: Verificação de disponibilidade do servidor
O sistema SHALL verificar (health-check com timeout) que o `llama-server` está pronto pra receber requisições antes de liberar o gate de permissão do pipeline de conversão.

#### Scenario: Servidor ainda carregando o modelo
- **WHEN** o `llama-server` foi iniciado mas ainda não responde ao health-check
- **THEN** sistema exibe indicação de "carregando modelo..." e não libera os botões de permissão até o servidor responder ou o timeout expirar

#### Scenario: Timeout de inicialização
- **WHEN** o `llama-server` não fica disponível dentro do timeout configurado
- **THEN** sistema exibe mensagem de erro clara indicando falha na inicialização do servidor local

### Requirement: Encerramento automático do llama-server
Ao fechar o app (fechamento normal da janela ou saída do processo Python), o sistema SHALL encerrar o processo `llama-server` que ele mesmo iniciou.

#### Scenario: Usuário fecha a janela do app
- **WHEN** usuário fecha a janela principal do app
- **THEN** sistema envia sinal de término ao processo `llama-server` antes de finalizar

#### Scenario: App encerra por exceção não tratada
- **WHEN** o processo Python do app termina por uma exceção não tratada
- **THEN** sistema garante, via handler de saída, que o processo `llama-server` iniciado por ele também é encerrado
