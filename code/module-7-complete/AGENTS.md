# AGENTS.md

> Human-readable documentation of the AI agents in this project.
> For agent definitions, see `.github/agents/*.agent.md`

---

## Agent Philosophy

1. **Context is Attention** — What you feed the agent determines what it can reason about
2. **DARE Model** — Deterministic first, AI for ambiguity, Review at boundaries, Escalate on failure
3. **Tool Restrictions** — Each agent has limited capabilities by design
4. **Handoffs** — Agents pass work to each other at defined boundaries
5. **MCP for Documentation** — Access docs efficiently, don't memorize them

---

## Agent Team

| Agent | Type | Role | Tools | Model Tier |
|-------|------|------|-------|------------|
| **api-advisor** | Advisor | Teaching + MCP doc access | read, search, fetch, MCP | Balanced |
| **endpoint-generator** | Doer | Creates Flask routes | read, edit, terminal | Fast |
| **dto-builder** | Doer | Creates DTOs from schemas | read, edit | Fast |
| **strands-builder** | Doer | Builds Strands agents | read, edit, terminal, MCP | Balanced |
| **schema-validator** | Gate | Validates OpenAPI compliance | read, search | Fast |
| **reviewer** | Gate | Reviews API code | read, search, githubRepo | Balanced |

### Model Tier Principle

**Use the cheapest model that can do the job.**

| Tier | Cost | Use For |
|------|------|---------|
| **Fast** | $ | Structured tasks (route generation, schema validation) |
| **Balanced** | $$ | Nuanced reasoning (teaching, building agents, reviewing) |

---

## Agent Types

### Advisor Agents (Teaching)
- Help navigate API design decisions
- Use MCP to access documentation in real-time
- **Cannot modify code** — only guide
- Hand off to Doer agents when ready

### Doer Agents (Implementation)
- Write and modify code
- Run commands in terminal
- **Follow OpenAPI spec exactly**
- Hand off to Gate agents for review

### Gate Agents (Quality)
- **Read-only access** — cannot modify files
- Validate against OpenAPI spec
- Approve or reject changes
- Escalate issues to humans

---

## MCP Documentation Pattern

> 💡 **"10x Google Fu"** — Access documentation efficiently, don't memorize it.

| Topic | MCP Server |
|-------|------------|
| Strands patterns | strands-agents |
| AWS services | aws-docs |
| Flask patterns | filesystem (existing routes) |
| Project context | filesystem (HISTORY.md) |

---

## Handoff Pattern

```
Human provides task
    ↓
api-advisor explains/guides (with MCP)
    ↓
Human approves design
    ↓
Doer agent implements
    ↓
schema-validator validates
    ↓
reviewer checks
    ↓
Human approves
    ↓
Record in HISTORY.md
```

---

## DARE Model in APIs

| Letter | Principle | This Project |
|--------|-----------|--------------|
| **D** | Deterministic First | OpenAPI validation, linting, schema checks |
| **A** | AI for Ambiguity | Endpoint generation, agent reasoning |
| **R** | Review at Boundaries | API review before merge |
| **E** | Escalate on Failure | Timeout handling, fallbacks |

---

## Key Files

| Purpose | File |
|---------|------|
| Agent memory | `HISTORY.md` |
| API spec | `openapi/api-spec.yaml` |
| MCP config | `.vscode/mcp.json` |
| Architecture decisions | `docs/proposals/*.md` |

---

*Follows spec-driven AI development methodology.*
