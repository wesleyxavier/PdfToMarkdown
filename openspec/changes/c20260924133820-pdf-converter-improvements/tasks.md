## 0. Branch

- [ ] 0.1 Criar branch `feature/pdf-converter-improvements`

## 1. Persistência SQLite (Histórico)

- [ ] 1.1 Criar módulo `src/PdfToMarkdown/Infrastructure/history_db.py` com criação da tabela `conversions` e funções de gravação/atualização de histórico
- [ ] 1.2 Implementar testes unitários para gravação de histórico no SQLite

## 2. Pipeline de Conversão (Nomenclatura _convert.md, ZIP e Múltiplos Arquivos)

- [ ] 2.1 Atualizar `convert_pdf_to_markdown` para salvar o arquivo de saída como `{stem}_convert.md`
- [ ] 2.2 Implementar suporte a múltiplos PDFs com empacotamento em arquivo `.zip` quando houver mais de um documento convertido
- [ ] 2.3 Integrar o registro no banco SQLite ao ciclo de início e conclusão de cada conversão no pipeline
- [ ] 2.4 Atualizar testes unitários do pipeline para cobrir `_convert.md`, múltiplos arquivos e criação de ZIP

## 3. Interface Desktop CustomTkinter (Seleção Múltipla, Contador e Auto-Scroll)

- [ ] 3.1 Atualizar a interface gráfica: remover o botão "Buscar em Pasta" e atualizar o botão principal para "Selecionar arquivos PDF" com suporte a múltiplos arquivos (`askopenfilenames`)
- [ ] 3.2 Implementar contador de tempo decorrido em segundos em tempo real na bolha de status durante o envio da página para o modelo
- [ ] 3.3 Garantir o auto-scroll consistente até o fim da área de chat a cada nova mensagem ou atualização do contador

## 4. Testes e Qualidade

- [ ] 4.1 Executar a suíte de testes com `pytest`
- [ ] 4.2 Executar linter `ruff check .`
- [ ] 4.3 Atualizar documentação no `README.md`
- [ ] 4.4 Atualizar o grafo de conhecimento `graphify update .`

## 5. Finalização

- [ ] 5.1 Commit + push para o repositório remoto na branch `feature/pdf-converter-improvements`
