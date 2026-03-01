## Agent Definitions

### Agent Team Summary

| Agent | Type | Model Tier | Purpose | MCP Access |
|-------|------|------------|---------|------------|
| `api-advisor` | Advisor | Balanced | Teaching + documentation | ✅ All servers |
| `endpoint-generator` | Doer | Fast | Creates Flask routes | Filesystem only |
| `dto-builder` | Doer | Fast | Creates DTOs from schemas | Filesystem only |
| `strands-builder` | Doer | Balanced | Creates Strands agents | ✅ strands-agents |
| `schema-validator` | Gate | Fast | Validates OpenAPI compliance | Filesystem only |
| `reviewer` | Gate | Balanced | Reviews API code | Filesystem only |

### Schema-Validator Agent

```yaml
# .github/skills/schema-validator/SKILL.md
---
name: schema-validator
description: Validates API implementation against OpenAPI spec
tools:
  - read
  - search
model_tier: fast  # Validation is mechanical
---

# Schema Validator Agent

## Role
Validate that API implementation matches OpenAPI specification.
Read-only — cannot modify files.

## Process
1. Read `openapi/api-spec.yaml` for expected contract
2. Read route implementation in `src/routes/`
3. Compare:
   - Endpoint paths match
   - HTTP methods match
   - Request schemas match DTOs
   - Response schemas match DTOs
   - Error responses defined
4. Report discrepancies

## Restrictions
- Read-only — cannot modify files
- Cannot run tests (that's for humans/CI)
- Reports issues, doesn't fix them

## Handoffs
- Receives from: endpoint-generator, dto-builder
- Hands off to: Human (for approval or fixes)

## Validation Checklist

| Check | How |
|-------|-----|
| Path exists | Route decorator matches spec path |
| Method correct | GET/POST/PUT/DELETE matches |
| Request body | DTO fields match schema properties |
| Response body | to_dict() output matches schema |
| Status codes | All spec responses have handlers |
| Required fields | Validation enforces required |

## Output Format

```markdown
## Schema Validation Report

### ✅ Passed
- /predict POST: All checks passed
- /customers GET: All checks passed

### ⚠️ Warnings
- /customers POST: Missing 409 conflict response handler

### ❌ Failed
- /insights GET: Response missing 'model' field defined in spec
```
```

### Reviewer Agent

```yaml
# .github/skills/reviewer/SKILL.md
---
name: reviewer
description: Reviews API code for quality and patterns
tools:
  - read
  - search
  - githubRepo
model_tier: balanced  # Review requires judgment
---

# Reviewer Agent

## Role
Review API code for quality, patterns, and potential issues.
Read-only — provides feedback, doesn't modify code.

## Review Dimensions

| Dimension | What to Check |
|-----------|--------------|
| **Correctness** | Does it work? Edge cases? |
| **Patterns** | Follows project conventions? |
| **Security** | Input validation? Auth checks? |
| **Performance** | N+1 queries? Missing indexes? |
| **Maintainability** | Clear names? Documented? |

## Process
1. Read the file(s) to review
2. Check against project patterns (read existing code)
3. Check against OpenAPI spec
4. Provide structured feedback

## Restrictions
- Read-only — cannot modify files
- Cannot approve/merge (human decision)
- Focus on actionable feedback

## Handoffs
- Receives from: endpoint-generator, strands-builder, dto-builder
- Hands off to: Human (for final approval)

## Output Format

```markdown
## Code Review: src/routes/customers.py

### ✅ Looks Good
- Follows blueprint pattern
- Error responses consistent
- Pagination implemented correctly

### 💡 Suggestions
- Consider adding rate limiting comment for production
- Could extract validation to separate function

### ⚠️ Issues
- Missing docstring on create_customer()
- No test for duplicate email case

### Verdict
**Approve with suggestions** — no blocking issues
```
```

---

## Appendix

### A. Progressive Disclosure Summary

| Module | Disclosure Method | Example |
|--------|-------------------|---------|
| 1 | Decided to be read | api-advisor reads Course 3 artifacts |
| 2 | Discovered | endpoint-generator learns from existing routes |
| 3 | Decided to be read | dto-builder reads OpenAPI schemas |
| 4 | Triggered | Timeout handling activates fallback |
| 5 | **MCP documentation** | **Real-time documentation access** |
| 6 | Given in feedback | CDK synth errors guide fixes |
| 7 | All methods | Integration testing reveals issues |

### B. Enterprise Context Summary

| Module | Enterprise Reality |
|--------|-------------------|
| 1 | Model serving latency requirements |
| 2 | API versioning, authentication, rate limiting |
| 3 | Connection pooling, database migrations |
| 4 | Agent costs, timeouts, fallback behavior |
| 5 | MCP for internal documentation, team scaling |
| 6 | Drift detection, compliance, multi-cloud strategy |
| 7 | CI/CD, staging environments, rollback procedures |

### C. Checkpoint Tags

```bash
git checkout module-1-setup      # Environment ready, model integrated
git checkout module-2-flask      # Flask fundamentals complete
git checkout module-3-database   # SQLite integration complete
git checkout module-4-strands    # Strands agents complete
git checkout module-5-mcp        # MCP "10x Google Fu" complete
git checkout module-6-cdk        # CDK introduction complete
git checkout module-7-complete   # Full integration, ready for Course 5
```

### D. MCP Server Quick Reference

| Server | Command | Use For |
|--------|---------|---------|
| strands-agents | `uvx strands-agents-mcp-server` | Strands documentation |
| aws-docs | `uvx awslabs.aws-documentation-mcp-server` | AWS documentation |
| web-search | `uvx mcp-server-brave-search` | General web fallback |
| filesystem | `npx @modelcontextprotocol/server-filesystem .` | Project files |

### E. Key Files Reference

| File | Purpose | Updated By |
|------|---------|------------|
| `HISTORY.md` | Project narrative, agent memory | Agents + Human |
| `CHANGELOG.md` | Release notes | Human only |
| `AGENTS.md` | Agent team documentation | Human |
| `openapi/api-spec.yaml` | API contract | Human (authoritative) |
| `docs/proposals/*.md` | Architecture decisions | Human + api-advisor |

---

## What's Next: Course 5 Preview

**Course 5: DevOps & Deployment** takes everything we built and deploys it to production:

| Course 4 Foundation | Course 5 Addition |
|---------------------|-------------------|
| Flask API (local) | Lambda/ECS (cloud) |
| SQLite | RDS PostgreSQL |
| Manual testing | CI/CD automation |
| CDK foundation | Full infrastructure |
| Basic health check | CloudWatch monitoring |
| No auth | Cognito authentication |

**Patterns that continue:**
- `devops-advisor` reads HISTORY.md for context
- Progressive disclosure with 💡 callouts
- Enterprise context with 🏢 callouts
- DARE model for deployment decisions
- Proposal pattern for infrastructure choices

---

*Course 4 of the Spec-Driven AI Development series.*  
*[← Course 3: ML Pipelines](https://github.com/andrewwint/spec-driven-ai-dev-03-ml-pipelines)*  
