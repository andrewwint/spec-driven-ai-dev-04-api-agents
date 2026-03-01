# Project History

This file captures the project narrative, decisions, and context.
It serves as persistent memory for AI agents across sessions.

---

## Course 4: API & Agent Development

**Continuing from Course 3:** Integrating fraud detection model into a production API.

---

## Decisions Made

### Framework: Flask
- **Selected:** Flask
- **Rationale:** Teaches patterns that transfer to FastAPI
- **Trade-off:** FastAPI has better async support, but patterns identical

### Database: SQLite → PostgreSQL
- **Selected:** SQLite for local development
- **Rationale:** Zero setup, no credentials needed
- **Upgrade path:** Environment variable switches to PostgreSQL

### AI Agents: Strands
- **Selected:** Strands Agents
- **Rationale:** Model-agnostic, simpler than LangChain
- **Model:** Claude Haiku (cheapest that works)

### Infrastructure: CDK
- **Selected:** AWS CDK
- **Rationale:** Python-based, generates CloudFormation
- **Trade-off:** AWS-only, but concepts transfer to Terraform

---

## Implementation Summary

### /predict Endpoint
- Wraps Course 3's FraudPredictor
- Validates against feature_schema.yaml
- Lazy model loading (once at startup)

### /customers Endpoints
- CRUD operations with SQLite
- DTOs control what crosses API boundary
- created_at intentionally not exposed

### /insights Endpoint
- Strands agent for customer analysis
- 30-second timeout with 504 fallback
- Tools: get_customer_info, get_prediction_history, get_fraud_statistics

### CDK Foundation
- Lambda + API Gateway stack (not deployed)
- Foundation for Course 5 full deployment

---

## Course 5 Handoff

**Artifacts ready:**
- Flask API: `src/app.py` + routes
- Strands agents: `src/agents/`
- CDK foundation: `cdk/`
- SQLite schema: `src/database/db.py`
- OpenAPI spec: `openapi/api-spec.yaml`

---

> 💡 **For future agents:** Read this file to understand project context.
