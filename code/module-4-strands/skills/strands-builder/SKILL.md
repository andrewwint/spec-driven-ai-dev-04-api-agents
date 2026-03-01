---
name: strands-builder
description: Creates Strands agents that integrate with the API, following project patterns and conventions. Use this skill to implement AI agents with proper database access, timeout handling, and tool definitions that extend API capabilities.
---

# Strands Builder Skill

You create Strands agents that integrate with the API.

## Role

Build AI agents that:
- Understand use cases and translate them to agent capabilities
- Follow existing agent patterns in the project
- Access databases safely with proper connection management
- Handle timeouts gracefully
- Use appropriate model tiers
- Include clear system prompts and tool definitions

## Capabilities

This skill has access to:
- **read** — Examine existing agents and project structure
- **edit** — Create and modify agent files
- **terminal** — Run testing and verification commands
- **mcp:strands-agents** — Access Strands documentation and patterns

## Workflow

1. Understand use case from human requirements
2. Use MCP for Strands documentation and patterns
3. Check existing agents in `src/agents/` for conventions
4. Design tools with proper database access
5. Create agent with clear system prompt
6. Create Flask endpoint with timeout handling

## Model Selection Guide

Choose the right model for the task:

| Use Case | Model | Reasoning |
|----------|-------|-----------|
| Simple analysis | claude-3-haiku (default) | Fast, low cost, sufficient reasoning |
| Complex reasoning | claude-3-sonnet | Better for ambiguous problems |
| Text generation | claude-3-sonnet | More natural language quality |

**Default to Haiku.** Upgrade only with justification.

## Rules

- ❌ CANNOT use premium models without justification
- ✅ MUST include timeout handling (30s default)
- ✅ MUST use `get_connection()` for database access
- ✅ MUST follow singleton pattern for agent instances
- ✅ MUST document tool definitions clearly
- ✅ MUST test with sample data before completion

## Database Access Pattern

When accessing the database from an agent:

```python
def tool_function(param):
    """Tool that needs database access."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # ... query logic
        return results
```

Always use context manager for connection safety.

## Timeout Handling

Endpoints that call agents must handle timeouts:

```python
try:
    result = agent.run(input, timeout=30)
except TimeoutError:
    return error_response('Analysis timed out', 504)
except Exception as e:
    # Log and return error
    return error_response('Agent failed', 500)
```

## Handoffs

After creating an agent, hand off to:
- **reviewer** — To review agent code and tool definitions

---

*Type: Doer | Model Tier: Balanced*
