# Spec-Driven AI Development — Course 4: API Agents for AI Pipelines

Build, deploy, and integrate API agents for production ML pipelines using spec-driven methodology.

## Prerequisites

- **Course 1: Foundations** (required)
- **Course 2: Data Platform** (required)
- **Course 3: ML Pipelines** (required)
- Python 3.11+
- VS Code with GitHub Copilot

## How To Use This Repo

Each folder in `code/` is a **complete snapshot** of the project at that module's checkpoint. You don't build on the previous folder — each one stands alone.

**Option A: Follow along**  
Download `attachments/course-4-api-agents.zip`, unzip it, and build alongside the lectures.
**Option B: Jump to a module**  
Copy any module folder as your starting point:

```bash
cp -r code/module-3-database/ my-project/
cd my-project/
```

**Option C: Compare your work**  
Diff your project against the reference:

```bash
diff -r my-project/ code/module-5-mcp/
```

## Course Modules

| #   | Module                    | Folder               | Duration |
| --- | ------------------------- | -------------------- | -------- |
| 1   | Model Integration & Setup | `module-1-setup/`    | 90 min   |
| 2   | Flask Fundamentals        | `module-2-flask/`    | 90 min   |
| 3   | Database Integration      | `module-3-database/` | 90 min   |
| 4   | Strands Agents            | `module-4-strands/`  | 90 min   |
| 5   | MCP Documentation         | `module-5-mcp/`      | 75 min   |
| 6   | CDK & Cloud               | `module-6-cdk/`      | 75 min   |
| 7   | Full Integration          | `module-7-complete/` | 75 min   |

**Total: ~9 hours**

## What You'll Build

- **API agent:** FastAPI-based service for ML model serving
- **MCP server:** Real-time documentation and tool chaining
- **Full documentation:** API proposals, config references, OpenAPI contracts

## Agent Team

| Agent              | Type    | Model Tier | Purpose                                 |
| ------------------ | ------- | ---------- | --------------------------------------- |
| api-advisor        | Advisor | Balanced   | Teaches API concepts (read-only)        |
| endpoint-generator | Doer    | Fast       | Generates endpoints, learns from routes |
| dto-builder        | Doer    | Fast       | Builds DTOs from OpenAPI schemas        |
| fallback-handler   | Gate    | Fast       | Handles timeouts, fallback logic        |
| reviewer           | Gate    | Balanced   | Reviews API proposals (read-only)       |

## Tech Stack

| Tool           | Purpose                    |
| -------------- | -------------------------- |
| Python 3.11+   | API development            |
| FastAPI        | API framework              |
| YAML           | API contracts              |
| Docker         | Containerization           |
| VS Code        | IDE + AI host              |
| GitHub Copilot | Agent runtime              |
| Make           | Deterministic verification |
| pytest         | API testing                |
| ruff           | Python linting/formatting  |

## Series Overview

This is **Course 4 of 5** in the Spec-Driven AI Development series:

| Course            | Focus                    | Status             |
| ----------------- | ------------------------ | ------------------ |
| 1. Foundations    | Thinking in Chunks       | ✅ Prerequisite    |
| 2. Data Platform  | Advisor Pattern          | ✅ Prerequisite    |
| 3. ML Pipelines   | Experiments as Proposals | ✅ Prerequisite    |
| **4. API Agents** | **Production Services**  | **← you are here** |
| 5. DevOps         | CI/CD + Deployment       | Coming             |

**Connects From:** Course 3 provides trained model, `predict.py`, API contract, model card.

**Connects To:** Course 5 receives production API, monitoring, and deployment patterns.

## Industry Context

We teach principles that transfer to industry tools:

| We Teach               | Industry Equivalent |
| ---------------------- | ------------------- |
| API proposals          | OpenAPI/Swagger     |
| MCP server             | Internal API docs   |
| Makefile orchestration | CI/CD pipelines     |
| Model handoff          | Model registry      |

## Udemy Course

👉 [Spec-Driven AI Development: API Agents for AI Pipelines](#)

## License

[Choose your license]
