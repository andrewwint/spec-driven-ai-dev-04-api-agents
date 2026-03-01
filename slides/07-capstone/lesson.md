## Module 7: Integration & Handoff (0.75 hrs)

### Learning Objectives
- Integrate all Course 4 components
- Run full test suite
- Prepare artifacts for Course 5
- Review the course journey

---

### 7.1 Full Integration Test (20 min)

**Concept:** Verify all components work together.

#### Integration Test Flow

```
┌────────────────────────────────────────────────────────────────┐
│                   INTEGRATION TEST FLOW                         │
│                                                                 │
│   1. Initialize database                                        │
│      $ make init-db                                            │
│                                                                 │
│   2. Start Flask app                                           │
│      $ make run                                                │
│                                                                 │
│   3. Test /predict endpoint (Course 3 model)                   │
│      $ curl -X POST localhost:5000/api/v1/predict ...          │
│                                                                 │
│   4. Test /customers CRUD (SQLite)                             │
│      $ curl localhost:5000/api/v1/customers                    │
│                                                                 │
│   5. Test /insights agent (Strands)                            │
│      $ curl localhost:5000/api/v1/insights/1                   │
│                                                                 │
│   6. Verify OpenAPI compliance                                 │
│      $ make lint-openapi                                       │
│                                                                 │
│   7. Run full test suite                                       │
│      $ make test                                               │
└────────────────────────────────────────────────────────────────┘
```

#### Test Commands

```makefile
# Makefile targets for integration testing

.PHONY: test test-predict test-api test-agents lint-openapi verify

test:
	pytest tests/ -v

test-predict:
	pytest tests/test_predict.py -v

test-api:
	pytest tests/test_routes.py -v

test-agents:
	pytest tests/test_agents.py -v

lint-openapi:
	openapi-spec-validator openapi/api-spec.yaml

verify: lint lint-openapi test
	@echo "All checks passed!"
```

#### Integration Test File

```python
# tests/test_integration.py
"""
Integration tests verifying all components work together.
"""

import pytest
from src.app import create_app
from src.database.db import reset_db


@pytest.fixture
def app():
    """Create app with test configuration."""
    app = create_app({
        'TESTING': True,
        'DATABASE_PATH': 'data/test.db'
    })
    
    with app.app_context():
        reset_db()
    
    yield app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


class TestPredictEndpoint:
    """Test Course 3 model integration."""
    
    def test_predict_valid_input(self, client):
        """Model should return prediction for valid input."""
        response = client.post('/api/v1/predict', json={
            'amount': 1500.00,
            'merchant_category': 'retail',
            'time_since_last': 120
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['prediction'] in ['fraud', 'legitimate']
        assert 0 <= data['confidence'] <= 1
        assert data['model_version'] == 'fraud_classifier_v1'
    
    def test_predict_missing_required_field(self, client):
        """Should return 400 for missing required field."""
        response = client.post('/api/v1/predict', json={
            'merchant_category': 'retail'
            # missing 'amount'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data


class TestCustomersEndpoint:
    """Test customer CRUD operations."""
    
    def test_create_and_list_customers(self, client):
        """Should create and retrieve customers."""
        # Create
        response = client.post('/api/v1/customers', json={
            'name': 'Alice Test',
            'email': 'alice@test.com'
        })
        assert response.status_code == 201
        
        # List
        response = client.get('/api/v1/customers')
        assert response.status_code == 200
        data = response.get_json()
        assert data['total'] >= 1


class TestInsightsEndpoint:
    """Test Strands agent integration."""
    
    def test_insights_requires_customer(self, client):
        """Should return 404 for non-existent customer."""
        response = client.get('/api/v1/insights/99999')
        
        assert response.status_code == 404
    
    @pytest.mark.slow  # Mark slow tests for optional skip
    def test_insights_returns_analysis(self, client):
        """Should return AI analysis for existing customer."""
        # Create customer first
        client.post('/api/v1/customers', json={
            'name': 'Bob Test',
            'email': 'bob@test.com'
        })
        
        response = client.get('/api/v1/insights/1')
        
        # May timeout in CI, so accept 200 or 504
        assert response.status_code in [200, 504]
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'insights' in data
```

**Hands-On:**
- Run `make test` — all should pass
- Manually test each endpoint with curl
- Verify agent responses are reasonable

---

### 7.2 Course 5 Handoff (20 min)

**Concept:** Understand what Course 5 receives and how to prepare.

#### Artifacts for Course 5

| Artifact | Location | Course 5 Use |
|----------|----------|--------------|
| Flask API | `src/app.py` + routes | Deploy to Lambda/ECS |
| Strands agents | `src/skills/` | Deploy agent infrastructure |
| CDK foundation | `cdk/` | Extend with full deployment |
| OpenAPI spec | `openapi/api-spec.yaml` | API Gateway configuration |
| SQLite schema | `src/database/db.py` | Migrate to RDS/Aurora |
| HISTORY.md | Root | Context for devops-advisor |
| Proposals | `docs/proposals/` | Decision rationale |

#### What Course 5 Adds

| Course 4 (This Course) | Course 5 (DevOps) |
|------------------------|-------------------|
| Flask app running locally | Flask on Lambda/ECS |
| SQLite database | RDS PostgreSQL |
| CDK stack (not deployed) | Full deployment pipeline |
| Strands agents | Agent infrastructure |
| Manual testing | CI/CD automation |
| Local MCP servers | Production monitoring |

#### Handoff Checklist

```markdown
## Course 5 Handoff Checklist

### Code Artifacts
- [ ] Flask app starts without errors (`make run`)
- [ ] All tests pass (`make test`)
- [ ] OpenAPI spec validates (`make lint-openapi`)
- [ ] CDK synthesizes without errors (`cd cdk && cdk synth`)

### Documentation
- [ ] HISTORY.md updated with all decisions
- [ ] AGENTS.md lists all agents with roles
- [ ] Proposals document architecture decisions
- [ ] README.md has setup instructions

### Environment
- [ ] requirements.txt complete
- [ ] Environment variables documented
- [ ] MCP servers configured in .vscode/mcp.json

### Ready for Deployment
- [ ] Lambda handler created (lambda_handler.py)
- [ ] Database migration path documented
- [ ] Agent timeout configured appropriately
```

> 💡 **Progressive Disclosure:** Course 5's `devops-advisor` will read your `HISTORY.md` to understand decisions made here. Keep it detailed!

**Hands-On:**
- Review HISTORY.md completeness
- Verify all artifacts are present
- Run final `make verify`

---

### 7.3 Course Review (15 min)

**Concept:** Review the journey and key takeaways.

#### What You Built

```
api-service/
├── src/
│   ├── app.py              # Flask application
│   ├── ml/predict.py       # Course 3 integration ← FROM COURSE 3
│   ├── routes/
│   │   ├── predict.py      # /predict endpoint (model)
│   │   ├── customers.py    # /customers CRUD
│   │   └── insights.py     # /insights agent
│   ├── models/
│   │   └── customer.py     # DTOs
│   ├── skills/
│   │   └── customer_insights.py  # Strands agent
│   └── database/
│       └── db.py           # SQLite + upgrade path
├── cdk/
│   └── stacks/
│       └── api_stack.py    # Infrastructure foundation
├── openapi/
│   └── api-spec.yaml       # API contract
├── docs/
│   └── proposals/          # Architecture decisions
├── tests/                   # Test suite
└── .github/skills/         # Agent team
    ├── api-advisorSKILL.md        # Advisor with MCP
    ├── endpoint-generatorSKILL.md # Doer
    ├── dto-builderSKILL.md        # Doer
    ├── strands-builderSKILL.md    # Doer
    ├── schema-validatorSKILL.md   # Gate
    └── reviewerSKILL.md           # Gate
```

#### Key Skills Acquired

| Skill | What You Learned | Transfers To |
|-------|------------------|--------------|
| Flask patterns | Blueprints, factory pattern | FastAPI, Express, any framework |
| SQLite → PostgreSQL | Connection management, migrations | Any database migration |
| Strands agents | Tools, system prompts, timeouts | LangChain, any orchestration |
| **MCP documentation** | **"10x Google Fu" skill** | **Any technology, forever** |
| CDK basics | IaC thinking, stacks, resources | Terraform, CloudFormation |

#### The Key Skill: "10x Google Fu"

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE KEY TAKEAWAY                              │
│                                                                  │
│   You don't need to memorize documentation.                     │
│   You need to know how to ACCESS it efficiently.                │
│                                                                  │
│   This skill transfers to:                                       │
│   • Learning new frameworks                                      │
│   • Debugging unfamiliar code                                   │
│   • Evaluating technology options                               │
│   • Staying current as things change                            │
│   • Onboarding to new projects                                  │
│   • Helping teammates with questions                            │
│                                                                  │
│   The habit:                                                     │
│   Question → api-advisor with MCP → Cited Answer                │
│   NOT: Question → Google → 10 tabs → Maybe find answer          │
└─────────────────────────────────────────────────────────────────┘
```

#### Course Journey Summary

| Module | What You Did | Key Concept |
|--------|--------------|-------------|
| 1 | Imported Course 3, setup environment | APIs as context boundaries |
| 2 | Built Flask routes, endpoint-generator | Blueprint organization |
| 3 | Added SQLite, DTOs | Database patterns transfer |
| 4 | Created Strands agent | When to use AI in APIs |
| 5 | Configured MCP servers | **"10x Google Fu"** ⭐ |
| 6 | Created CDK foundation | Infrastructure as code |
| 7 | Integrated, tested, prepared handoff | Course 5 ready |

---

### Module 7 Checkpoint

**By end of Module 7, you have:**
- ✅ All components integrated and tested
- ✅ Artifacts prepared for Course 5
- ✅ HISTORY.md updated with full project context
- ✅ Understanding of what comes next

**Git tag:** `module-7-complete`

**Final HISTORY.md Entry:**
```markdown
## Course 4 Complete — Ready for Course 5

### What Was Built
- Flask API with Course 3 model integration
- SQLite database with cloud upgrade path
- Strands customer insights agent
- MCP documentation access ("10x Google Fu")
- CDK infrastructure foundation (not deployed)

### Key Skills Acquired
1. API design with context boundaries
2. Flask patterns that transfer to any framework
3. Database patterns that transfer to any SQL
4. Strands agents (transfers to LangChain)
5. **MCP documentation access — the key skill**
6. Infrastructure as code thinking

### Decisions Made
- Flask over FastAPI (patterns transfer)
- SQLite for local dev (PostgreSQL path documented)
- Strands for model-agnostic AI
- CDK for infrastructure as code
- Haiku model for cost efficiency

### Ready for Course 5
All artifacts in place:
- Flask API: src/app.py + routes
- Strands agents: src/skills/
- CDK foundation: cdk/
- OpenAPI spec: openapi/api-spec.yaml
- SQLite schema: src/database/db.py
- HISTORY.md: Full project context

### What Course 5 Will Do
- Deploy to AWS (Lambda/ECS)
- Migrate SQLite → RDS PostgreSQL
- Add authentication (Cognito)
- Set up CI/CD (CodePipeline)
- Add monitoring (CloudWatch)
```

---

