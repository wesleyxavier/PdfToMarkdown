## ADDED Requirements

### Requirement: Registro de histórico de conversão em SQLite
O sistema SHALL persistir no banco de dados SQLite local (`history.db`) o histórico de cada arquivo PDF submetido para conversão.

#### Scenario: Gravação de conversão concluída com sucesso
- **WHEN** um arquivo PDF tem sua conversão finalizada
- **THEN** o sistema grava registro na tabela `conversions` contendo nome do arquivo, caminho original, caminho do arquivo gerado, quantidade de páginas, nome do computador, carimbos de data/hora (início e término), duração em segundos e status 'SUCCESS'

#### Scenario: Gravação de conversão com falha ou cancelamento
- **WHEN** o pipeline de conversão é interrompido por erro ou recusa no gate
- **THEN** o sistema grava ou atualiza o registro com o status correspondente ('FAILED' ou 'CANCELLED') e a descrição do erro (se houver)
