# PdfToMarkdown

Fonte única de conteúdo gerenciado deste projeto (design.md D2 da change
`genova-cli-project-generator`). `CLAUDE.md`, `AGENTS.md` e `GEMINI.md`
importam este arquivo como primeira linha — não duplique este conteúdo neles.

## Identidade

- Projeto: `PdfToMarkdown`
- Stack: `python`
- Gerado por: `genova` v1.5.1

---

## ⛔ REGRA ABSOLUTA

### DESENVOLVIMENTO SEM AUTORIZAÇÃO

**NUNCA dê commit, push ou PR sem autorização explícita e direta.**
**NUNCA inicie implementação de código, criação de arquivos, refatoração ou qualquer mudança no repositório sem que:**

1. Exista uma change ativa no OpenSpec (`openspec/changes/<nome>/`) com `tasks.md` aprovado pelo usuário
2. O usuário tenha dado autorização **explícita e direta** nesta conversa para iniciar a implementação

Ignorar esta regra — mesmo que o usuário pareça estar pedindo algo simples — é uma violação crítica. Em caso de dúvida, **pergunte antes de codar**.

### Fluxo obrigatório

1. Proposta → `/opsx:propose` → usuário revisa e aprova
2. Só então implementar, task a task, seguindo o `tasks.md`
3. Todo `tasks.md` deve iniciar (como `## 0. Branch`) com a criação de um **git worktree** para a branch:
   - **Sempre usar worktree** — nunca `git checkout -b` diretamente no workspace principal
   - Nomenclatura: `feature/{nome}`, `bugfix/{nome}` ou `hotfix/{nome}` conforme o tipo
   - Worktree criado em `worktrees/{branch}/` dentro do projeto (ignorado no `.gitignore`)
   - Verificar se a change anterior já foi concluída e está **mergeada em `develop`** com build passando
   - Se sim → worktree a partir de `develop`:

     ```bash
     git worktree add worktrees/{branch} -b feature/{branch} develop
     ```

   - Se não → perguntar ao usuário qual base usar. Nunca assumir a origem.
   - Após o usuário aprovar e mergear o PR → executar `/opsx:archive`, commitar em `develop` e remover o worktree:

     ```bash
     git worktree remove worktrees/{branch}
     ```

4. Todo `tasks.md` deve conter, de forma explícita e checável:
   - Ao final de cada grupo de tarefas: uma task própria de **commit + push** do grupo (dentro do worktree)
   - Antes da task de PR: uma task própria de **atualizar o README.md** do projeto
   - Antes da task de PR: executar **`graphify update .`** (AST-only, sem custo de API)
   - Como última task: **commit final + push + criar PR** com origem `feature/{nome}` → destino `develop`

### Orquestração multi-agente (via `/opsx:apply` e `/opsx:apply-parallel`)

Quando uma change possui `tasks.md` aprovado:

1. **Líder Técnico** avalia se as tasks podem ser divididas em tarefas paralelas (sem dependência sequencial)
2. Se sim: define contrato de interface entre partes, meta de cobertura dinâmica por tipo de código, e cria N agentes Dev Test (um por tarefa paralela)
3. Se não: conduz um único ciclo Dev Test/Dev Executor sequencial
4. **Dev Test + Dev Executor** (pool dinâmico): ciclo BDD-first (cenário → implementação → testes sequenciais → suíte completa → commit por tarefa)
5. **Dev Integrador**: aguarda todas as tarefas paralelas, verifica consistência, builda o projeto completo, faz commit final + push
6. **SecOps**: revisa código consolidado (leaks, credenciais, arquitetura), cria PR se aprovado
7. **Pipeline CI**: reexecuta suíte unit + funcional, valida cobertura contra meta definida pelo Líder Técnico, bloqueia merge se meta não atingida

Convenções:

- `.Tests/{worktree}/{frontend|backend}/{unit|e2e|integration|functional}/` — pasta gitignored para evidências (vídeos WebM, relatórios de cobertura)
- Plano `.md` de cada Dev Executor: identidade, items do `tasks.md` cobertos, checklist de subpassos como state machine retomável
- Papéis implementados via `Agent` tool do Claude Code (subagentes), sem orquestrador externo

### Testes obrigatórios

Toda implementação deve ser acompanhada de testes: **unitários sempre** (backend e frontend) + **integração sempre** (backend) + **funcional via unitário sempre** (backend) + **e2e funcionais sempre** (fluxo completo do usuário, backend e frontend).

### Padrão de Naming — OpenSpec Changes

Ao criar uma nova change com `/opsx:propose`, sempre use timestamp no início do nome:

```text
c<YYYYMMDDhhmmss>-<nome-da-change>
```

- `c` = prefixo obrigatório (OpenSpec rejeita nomes que começam com número)
- Timestamp = `yyyyMMddHHmmss`
- Nome = kebab-case descritivo

Na branch feature, **remover o timestamp**: `feature/nome-da-change`.

### 🐳 Docker Isolation — Regra Obrigatória

**Todo desenvolvimento Java/Kotlin/Mobile deve ser inteiramente Docker-based:**

- ❌ **NUNCA** assumir que SDKs (JDK, Android SDK), emulators, ou qualquer runtime está instalado localmente
- ✅ **Sempre** usar Docker containers para: compilação, testes, debugging, simulação, execução
- ✅ **Explícito em specs**: cada spec que envolva Java/Kotlin/Mobile DEVE mencionar Docker como requisito
- ✅ **Tasks precisam**: scripts de setup Docker, `docker-compose.yml`, ou equivalente

**Esta regra de arquitetura prevalece sobre qualquer outra preferência.**

---

## Estrutura do projeto

```text
├── .genova/   # Conteúdo gerenciado pelo genova CLI (rules.md)
├── openspec/   # Changes e specs OpenSpec do projeto
```

---

## Skills

Skills de stack e ai-history são mantidas centralmente no genovabase e
espelhadas nos agentes globais — não duplicadas por projeto. Consulte
`~/.ia/SKILLS/` (referência) ou invoque via Skill tool do agente.

## graphify

Este projeto tem (ou terá) um grafo de conhecimento em `graphify-out/`.

- Pra perguntas sobre o código, rode `graphify query "<pergunta>"` antes de
  grep bruto — retorna um subgrafo focado, geralmente bem menor que
  `GRAPH_REPORT.md`
- Use `graphify path "<A>" "<B>"` pra relações e `graphify explain "<conceito>"`
  pra conceitos focados
- Leia `graphify-out/GRAPH_REPORT.md` só pra revisão ampla de arquitetura
- Depois de mudar código, rode `graphify update .` pra manter o grafo atual
  (AST-only, sem custo de API)

## RTK

Comandos Bash passam pelo hook do RTK (Rust Token Killer) quando configurado
globalmente — filtragem de output é transparente, não requer ação do projeto.

@../../../../../../../../../.ia_history/INDEX.md
