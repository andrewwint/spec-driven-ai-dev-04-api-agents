# Course 4: API & Agent Development — Slide Modules

This directory contains per-module lesson slides for Course 4. Each module is a self-contained markdown file that can be used for teaching, presentations, or self-study.

## Module Index

| Module | File | Duration | Focus | Hands-On |
|--------|------|----------|-------|----------|
| **Overview** | [00-overview-lesson.md](./00-overview-lesson.md) | — | Course structure, throughline, skill definitions | — |
| **1** | [01-setup-lesson.md](./01-setup-lesson.md) | 1.5 hrs | Environment setup, Course 3 bridge, OpenAPI intro | Medium |
| **2** | [02-flask-lesson.md](./02-flask-lesson.md) | 1.5 hrs | Flask fundamentals, routes, blueprints, patterns | **High** |
| **3** | [03-database-lesson.md](./03-database-lesson.md) | 1.5 hrs | SQLite, DTOs, database patterns, cloud path | **High** |
| **4** | [04-strands-lesson.md](./04-strands-lesson.md) | 1.5 hrs | Strands agents in API, integration patterns | **High** |
| **5** | [05-mcp-lesson.md](./05-mcp-lesson.md) | 1.25 hrs | MCP documentation servers, "10x Google Fu" ⭐ KEY | Medium |
| **6** | [06-cdk-lesson.md](./06-cdk-lesson.md) | 1.0 hr | CDK introduction, infrastructure as code | Low |
| **7** | [07-capstone-lesson.md](./07-capstone-lesson.md) | 0.75 hrs | Integration, handoffs, Course 5 prep | Low |
| **References** | [appendices-reference.md](./appendices-reference.md) | — | Skill definitions and appendices | — |

**Total Course Duration: ~9 hours**

---

## Quick Navigation

### By Learning Path

#### Full Course (All Modules)
Best for: Developers new to APIs and agents
1. [Overview](./00-overview-lesson.md)
2. [Module 1: Setup](./01-setup-lesson.md)
3. [Module 2: Flask](./02-flask-lesson.md)
4. [Module 3: Database](./03-database-lesson.md)
5. [Module 4: Strands](./04-strands-lesson.md)
6. [Module 5: MCP](./05-mcp-lesson.md)
7. [Module 6: CDK](./06-cdk-lesson.md)
8. [Module 7: Capstone](./07-capstone-lesson.md)

#### Fast Track (~4 hours)
Best for: Experienced API developers
1. [Overview](./00-overview-lesson.md) — Quick skim
2. [Module 1.3: Context Boundaries](./01-setup-lesson.md#13-apis-as-context-boundaries) — Key concept
3. [Module 4: Strands Agents](./04-strands-lesson.md) — AI integration
4. [Module 5: MCP](./05-mcp-lesson.md) — "10x Google Fu" ⭐ Don't skip
5. [Module 7: Capstone](./07-capstone-lesson.md) — Integration view

### By Topic

**APIs & Specifications**
- [Module 1: Setup & OpenAPI](./01-setup-lesson.md)
- [Module 3: Database & DTOs](./03-database-lesson.md)
- [References](./appendices-reference.md)

**Web Development**
- [Module 2: Flask Fundamentals](./02-flask-lesson.md)
- [Module 3: Database Integration](./03-database-lesson.md)

**AI & Agents**
- [Module 4: Strands Agents](./04-strands-lesson.md)
- [Module 5: MCP Documentation](./05-mcp-lesson.md)

**Infrastructure & Deployment**
- [Module 6: CDK Introduction](./06-cdk-lesson.md)

---

## Skill Definitions

This course uses **AgentSkills.io format** for skill definitions. See the parent directory `../skills/` for individual skill files:

- `../skills/api-advisor/SKILL.md` — Advisor for API design guidance
- `../skills/endpoint-generator/SKILL.md` — Doer for creating Flask routes
- `../skills/dto-builder/SKILL.md` — Doer for building DTOs
- `../skills/strands-builder/SKILL.md` — Doer for creating Strands agents
- `../skills/schema-validator/SKILL.md` — Gate for OpenAPI validation
- `../skills/reviewer/SKILL.md` — Gate for code review

---

## Key Concepts

### The Throughline

> **"Manage the LLM's context window like you manage your own attention."**

This metaphor connects all course modules:
- APIs are context boundaries (Module 1)
- DTOs control what crosses those boundaries (Module 3)
- MCP documentation servers bring context efficiently (Module 5)

### The DARE Model

| Letter | Principle | Course Context |
|--------|-----------|----------------|
| **D** | Deterministic First | OpenAPI validation, linting |
| **A** | AI for Ambiguity | Skill-assisted endpoint generation |
| **R** | Review at Boundaries | Code review before merge |
| **E** | Escalate on Failure | Error handling, timeouts |

### "10x Google Fu" (Module 5)

The key differentiator of this course is learning to use MCP documentation servers to access documentation efficiently without memorizing. This "10x Google Fu" skill applies across all your work.

---

## Using These Slides

### For Teaching
- Present one module per session
- Use checkboxes in each module to track progress
- Reference code examples directly from the repository
- Include hands-on exercises from each module

### For Self-Study
- Read one module per day
- Complete hands-on exercises as you go
- Reference AGENTS.md and HISTORY.md for context
- Use the fast-track path if you have prior API experience

### For Review
- Use the Overview to refresh your memory of the throughline
- Reference individual modules for specific topics
- Check appendices for skill definitions and standards

---

## Terminology Notes

This course uses **AgentSkills.io terminology**:
- `.agent.md` files are now `SKILL.md` in AgentSkills.io format
- `agents/` directory is now `skills/` for clarity
- "agent file" → "skill file" in documentation
- **Note:** "agent" as a general concept (AI agent) remains unchanged
- `AGENTS.md` stays as the project overview document

---

## Code Repositories

Course code is organized by module:
- `../code/module-1-setup/` — Environment setup
- `../code/module-2-flask/` — Flask application
- `../code/module-3-database/` — Database schema and DTOs
- `../code/module-4-strands/` — Strands agents
- `../code/module-5-mcp/` — MCP server setup
- `../code/module-6-cdk/` — Infrastructure as code
- `../code/module-7-complete/` — Complete working example

---

## Additional Resources

- **Project Documentation:** `../AGENTS.md` — Skill team overview and philosophy
- **Project History:** `../HISTORY.md` — Decisions and milestones
- **OpenAPI Spec:** `../openapi/api-spec.yaml` — API contract
- **Skill Definitions:** `../skills/*/SKILL.md` — AgentSkills.io format

---

*Course follows spec-driven AI development methodology. Last updated: March 2026.*
