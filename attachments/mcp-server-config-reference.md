# MCP Server Configuration Reference

## Required Settings

- `host`: Server host (e.g., 0.0.0.0)
- `port`: Server port (e.g., 8080)
- `model_path`: Path to model file
- `api_contract`: Path to API contract YAML

## Optional Settings

- `log_level`: DEBUG/INFO/WARN/ERROR
- `max_workers`: Number of worker threads
- `timeout`: Request timeout (seconds)

## Example

```yaml
host: 0.0.0.0
port: 8080
model_path: ./models/model.pkl
api_contract: ./docs/api-contract.yaml
log_level: INFO
max_workers: 4
timeout: 30
```
