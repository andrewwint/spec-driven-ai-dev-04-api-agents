# Proposal: Strands Agent Integration

## Summary

Add AI-powered customer insights via `/insights/{customer_id}` using Strands Agents.

## Design

```
GET /insights/1
    ↓
Verify customer exists (deterministic)
    ↓
Run Strands agent with 30s timeout
    ↓
Return analysis or 504 on timeout
```

## Agent Tools

| Tool | Purpose |
|------|---------|
| get_customer_info | Basic customer data |
| get_prediction_history | Recent predictions |
| get_fraud_statistics | Aggregated metrics |

## Model Selection

**Default:** Claude Haiku (~$0.25/1M tokens)
**Alternative:** Claude Sonnet (~$3/1M tokens) if Haiku insufficient

## Trade-offs

| Approach | Pros | Cons |
|----------|------|------|
| **Strands (chosen)** | Model-agnostic, simple | Smaller community |
| LangChain | Large community | More complex |
| Direct API | Full control | Reinvent patterns |

## Success Criteria

- [x] Agent uses all three tools
- [x] 30s timeout with 504 fallback
- [x] Model configurable via env var
