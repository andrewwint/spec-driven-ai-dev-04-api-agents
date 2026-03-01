# Proposal: Course 3 Model Integration

## Summary

Integrate Course 3's FraudPredictor into Flask API via `/predict` endpoint.

## Design

```
Request JSON → Flask Route → FraudPredictor → Response
                    ↓
              Validation against
              feature_schema.yaml
```

## Decision

- **Model Loading:** Lazy singleton (load once, reuse)
- **Validation:** Use FraudPredictor.validate() before predict()
- **Error Format:** Consistent with other endpoints

## Trade-offs

| Approach | Pros | Cons |
|----------|------|------|
| Load per request | Fresh model | Slow, expensive |
| **Singleton (chosen)** | Fast | Can't hot-reload |
| Global variable | Simple | Fails if file missing at import |

## Success Criteria

- [x] `/predict` returns valid predictions
- [x] Input validation matches schema
- [x] Model loads once per process
