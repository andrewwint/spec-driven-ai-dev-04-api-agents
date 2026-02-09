# Course 4: API & Agent Development

> **Core Message:** APIs are context boundaries. MCP documentation servers are skill multipliers. "10x your Google Fu."

[![Course 4](https://img.shields.io/badge/Course%204-API%20%26%20Agents-red)](https://github.com/andrewwint/spec-driven-ai-dev-04-api-agents)

---

## What You'll Build

A production-ready Fraud Detection API with:
- **Flask API:** REST endpoints wrapping Course 3's model
- **SQLite database:** Local-first with PostgreSQL upgrade path
- **Strands agents:** AI-powered customer insights
- **CDK foundation:** Infrastructure as code for Course 5

## What You're Really Learning

| Surface Topic | Actual Skill |
|---------------|--------------|
| Flask endpoints | Wrapping ANY function as a service |
| SQLite queries | Database patterns that transfer to any SQL |
| Strands agents | AI orchestration (transfers to LangChain) |
| MCP servers | **Efficient documentation access** — "10x Google Fu" |
| CDK basics | Infrastructure as code thinking |

**You are NOT becoming a Flask expert.** You're learning to use MCP to efficiently access documentation for ANY technology.

---

## Quick Start

```bash
git clone https://github.com/andrewwint/spec-driven-ai-dev-04-api-agents
cd spec-driven-ai-dev-04-api-agents
pip install -r requirements.txt
cp ../course-3-ml-pipelines/models/fraud_classifier_v1.pkl models/
make init-db
make run
```

---

## Fast Track (For API-Experienced Developers)

If you're comfortable with Flask and REST APIs:

| Skip To | What You'll Learn | Time |
|---------|-------------------|------|
| **Module 1.3** | "Context is attention" for APIs | 15 min |
| **Module 4** | Strands agents in APIs | 30 min |
| **Module 5** | MCP "10x Google Fu" ⭐ | 25 min |
| **Module 6.2** | CDK vs Terraform decisions | 15 min |

```bash
git checkout module-4-strands  # Start with Flask done
```

---

## Git Checkpoints

```bash
git checkout module-1-setup       # Environment, Course 3 integration
git checkout module-2-flask       # Flask app, /predict endpoint
git checkout module-3-database    # SQLite, DTOs, /customers
git checkout module-4-strands     # Strands agents, /insights
git checkout module-5-mcp         # MCP documentation servers
git checkout module-6-cdk         # Infrastructure as code
git checkout module-7-complete    # Ready for Course 5
```

---

## Project Structure

```
course-4-api-agents/
├── AGENTS.md              # Agent team documentation
├── HISTORY.md             # Project memory
├── openapi/               # API specification
├── src/
│   ├── app.py            # Flask application
│   ├── ml/               # Course 3 model integration
│   ├── routes/           # API endpoints
│   ├── models/           # DTOs
│   ├── database/         # SQLite
│   └── agents/           # Strands agents
├── cdk/                  # AWS CDK infrastructure
├── docs/proposals/       # Architecture decisions
└── .github/agents/       # Agent definitions
```

---

## Make Targets

```bash
make help          # Show all targets
make run           # Start Flask development server
make test          # Run all tests
make lint          # Run ruff linter
make lint-openapi  # Validate OpenAPI spec
make init-db       # Initialize SQLite database
```

---

## Connects From Course 3

**Required artifacts:**
- `models/fraud_classifier_v1.pkl` — Copy from Course 3

---

## Connects To Course 5

**Artifacts for deployment:**
- `src/app.py` — Flask app for Lambda/ECS
- `src/agents/` — Strands agents to deploy
- `cdk/` — Infrastructure foundation to extend
- `openapi/api-spec.yaml` — API Gateway config

---

*Part of the Spec-Driven AI Development course series.*
