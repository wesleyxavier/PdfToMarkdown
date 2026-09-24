# HARNESS — Personal Workspace

This file is the source of truth for the ecosystem. Covers context for humans and invariants for AI agents.

## ⛔ ABSOLUTE RULE

Governance rules and skills (authorization, workflow, worktree, branch-naming, openspec-naming, tasks-structure, docker-isolation, graphify-update) are **global** — they live in `~/.agents/rules/` and `~/.agents/skills/`, valid in any repo. See `~/*.md` §5.

---

## MCPs

**Skill**: Use `/azure-mcp-setup` for startup, config, and Agents Code integration.

---

## Local AI Usage: Llama cpp

**Skill**: Use `/llama-local-ai` for Docker setup, model configuration, and VSCode/Agents Code integration.

---

## graphify

**Skill**: Use `/graphify` for query/path/explain over the codebase.

**Rule**: `graphify-update.md` — run `graphify update .` before PR.

Knowledge graph at `graphify-out/` with god nodes, community structure, cross-file relationships.

---

## This Project

Infos in `README.md`

---

@.genova/rules.md
