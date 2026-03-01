## Module 1: Setup & Model Integration (1.5 hrs)

### Learning Objectives
- Configure the Course 4 development environment
- Import and verify Course 3 artifacts
- Understand APIs as context boundaries
- Draft initial OpenAPI specification

---

### 1.1 Course 3 Refresher — What Carries Forward (20 min)

**Concept:** Review patterns and artifacts from Course 3 that continue in this course.

#### Artifacts from Course 3

| Artifact | Location | How Course 4 Uses It |
|----------|----------|---------------------|
| Trained model | `models/fraud_classifier_v1.pkl` | Load in predict route |
| Prediction class | `src/ml/predict.py` | Wrap in Flask endpoint |
| API contract | `docs/api-contract.yaml` | Extend to `openapi/api-spec.yaml` |
| Feature schema | `docs/feature_schema.yaml` | Validate API inputs |
| Model card | `docs/model-card.md` | Document /predict endpoint |

#### Patterns That Continue

| Pattern | Course 3 | Course 4 |
|---------|----------|----------|
| Advisor Pattern | `ml-advisor` | `api-advisor` (same structure + MCP) |
| Progressive Disclosure | 💡 callouts | 💡 callouts (same format) |
| Enterprise Context | 🏢 callouts | 🏢 callouts (API-specific) |
| ROI Analysis | Model selection | API architecture decisions |
| Proposals | Experiment proposals | API design proposals |
| Agent Memory | HISTORY.md | HISTORY.md continues |

> 💡 **Progressive Disclosure:** You don't need to memorize what's in Course 3's artifacts. The `api-advisor` agent reads them when relevant. Ask it: *"What does Course 3's api-contract.yaml specify for the /predict endpoint?"*

**Hands-On:**
- Clone Course 4 starter repository
- Verify Course 3 artifacts are present
- Review `HISTORY.md` for project context

[📸 Screenshot: Repository structure showing Course 3 artifacts in place]

---

### 1.2 Environment Setup (25 min)

**Concept:** Configure the development environment with Flask, SQLite, and agent tooling.

#### Tech Stack Overview

| Tool | Purpose | Why This One |
|------|---------|--------------|
| Python 3.10+ | Runtime | Continues from Courses 1-3 |
| Flask | Web framework | Teaches patterns that transfer |
| SQLite | Database | Local-first, no credentials needed |
| Strands Agents | AI capabilities | Model-provider agnostic |
| uv | Package management | Fast, reliable |

#### Setup Steps

```bash
git clone https://github.com/andrewwint/spec-driven-ai-dev-04-api-agents
cd spec-driven-ai-dev-04-api-agents
git checkout start  # Module 1 starting point
uv pip install -r requirements.txt
```

#### Verify Installation

```bash
make verify  # Runs all checks
make test    # Should show Course 3 model loads correctly
```

> 🏢 **Enterprise Context:** In production, you'd use virtual environments or containers to isolate dependencies. SQLite works for development; Course 5 covers the PostgreSQL/RDS migration path.

**Hands-On:**
- Complete environment setup
- Run `make verify` successfully
- Load Course 3's model in Python REPL

[💻 Code: requirements.txt]
```txt
# Core
flask>=3.0.0
python-dotenv>=1.0.0

# Database
# SQLite is built-in to Python

# AI Agents
strands-agents>=0.1.0

# Course 3 Model Dependencies
scikit-learn>=1.3.0
pandas>=2.0.0
joblib>=1.3.0

# Development
pytest>=7.0.0
ruff>=0.1.0
```

---

### 1.3 APIs as Context Boundaries (25 min)

**Concept:** Connect the course throughline — "Context is Attention" — to API design.

#### The Throughline Connection

> **"Manage the LLM's context window like you manage your own attention."**

APIs do the same thing for services:
- Each endpoint defines **what context** the caller provides
- Each response defines **what context** the caller receives
- Well-designed APIs manage attention by exposing only relevant data

#### Context Boundaries in Practice

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONTEXT BOUNDARY                              │
│                                                                  │
│   Caller's Context          API Endpoint          Service Context │
│   ─────────────────         ────────────          ─────────────── │
│                                                                  │
│   • Customer ID      ─────►  /predict   ─────►   • Full model    │
│   • Transaction data                             • Feature eng   │
│   • Request metadata                             • All history   │
│                                                                  │
│   Caller doesn't need        Returns only:       API manages     │
│   to know about model        • prediction        what crosses    │
│   internals                  • confidence        the boundary    │
│                              • explanation                       │
└─────────────────────────────────────────────────────────────────┘
```

#### Why This Matters for AI Development

| Without Context Boundaries | With Context Boundaries |
|---------------------------|------------------------|
| Agents see everything | Agents see relevant context |
| Prompts bloat with irrelevant info | Focused, efficient prompts |
| Changes ripple everywhere | Changes isolated to service |

> 💡 **Progressive Disclosure:** This is why MCP documentation servers matter (Module 5). They let you pull documentation INTO your context only when relevant, rather than memorizing everything upfront.

**Hands-On:**
- Diagram the context boundary for the `/predict` endpoint
- Identify what Course 3's model needs vs. what the API exposes
- Draft input/output schemas showing the boundary

[📊 Diagram: Context boundary visualization for /predict endpoint]

---

### 1.4 Industry Context — Where This Fits (15 min)

**Concept:** Understand how this course's tools relate to industry standards.

#### What We Build vs. What Industry Uses

| Our Approach | Industry Standard | Why We Choose Ours |
|--------------|-------------------|-------------------|
| Flask | FastAPI, NestJS | Flask teaches patterns; FastAPI is same concepts |
| SQLite | PostgreSQL, RDS | Local-first, no credentials needed |
| Strands Agents | LangChain, LlamaIndex | Model-agnostic, simpler to teach |
| CDK intro | Terraform, Pulumi | AWS-native, real programming language |

#### The Principles Transfer

| Our Pattern | Transfers To |
|-------------|--------------|
| Flask blueprints | FastAPI routers, Express middleware |
| SQLite queries | Any SQL database |
| Strands agent definitions | LangChain agents (different syntax, same concepts) |
| CDK stacks | Terraform modules |

> 🏢 **Enterprise Context:** Your organization likely has standards. Learn Flask → understand FastAPI in a day. Learn CDK → understand Terraform concepts. **Patterns transfer; syntax doesn't matter.**

**Key Takeaway:**
You're NOT becoming a Flask expert. You're learning:
- How to wrap ANY function as a service
- Database patterns that transfer to any SQL
- AI orchestration concepts that work anywhere
- Infrastructure as code thinking

---

### 1.5 Model Integration — Wrapping FraudPredictor (25 min)

**Concept:** Bridge Course 3's ML model into a Flask endpoint.

#### Understanding the FraudPredictor Interface

First, let's understand what Course 3 gave us:

```python
# src/ml/predict.py (FROM COURSE 3)
"""
Course 3's FraudPredictor class.
DO NOT MODIFY — this is the interface we wrap.
"""

import joblib
import pandas as pd
from typing import Dict, Any

class FraudPredictor:
    """Fraud prediction model wrapper."""
    
    def __init__(self, model_path: str):
        """Load the trained model."""
        self.model = joblib.load(model_path)
        self.version = "fraud_classifier_v1"
    
    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a fraud prediction.
        
        Args:
            features: Dict matching feature_schema.yaml
                - amount: float
                - merchant_category: str
                - time_since_last: int
                - ... (see feature_schema.yaml for full list)
        
        Returns:
            Dict with:
                - prediction: "fraud" | "legitimate"
                - confidence: float (0.0 - 1.0)
                - features_used: list of feature names
        """
        # Feature engineering happens inside
        df = pd.DataFrame([features])
        
        prediction = self.model.predict(df)[0]
        probability = self.model.predict_proba(df)[0]
        
        return {
            "prediction": "fraud" if prediction == 1 else "legitimate",
            "confidence": float(max(probability)),
            "features_used": list(features.keys())
        }
```

#### Creating the /predict Endpoint

```python
# src/routes/predict.py
"""
Wraps Course 3's FraudPredictor in a Flask endpoint.
This is the bridge from ML Pipeline to API.
"""

from flask import Blueprint, request, jsonify
from src.ml.predict import FraudPredictor
import yaml

predict_bp = Blueprint('predict', __name__)

# Load model once at startup
predictor = FraudPredictor('models/fraud_classifier_v1.pkl')

# Load feature schema for validation
with open('docs/feature_schema.yaml', 'r') as f:
    FEATURE_SCHEMA = yaml.safe_load(f)


def validate_features(data: dict) -> list:
    """Validate request against Course 3's feature_schema.yaml."""
    errors = []
    
    for field, rules in FEATURE_SCHEMA.get('required_features', {}).items():
        if field not in data:
            errors.append(f"Missing required field: {field}")
        elif 'type' in rules:
            expected_type = rules['type']
            if expected_type == 'float' and not isinstance(data[field], (int, float)):
                errors.append(f"Field {field} must be numeric")
            elif expected_type == 'string' and not isinstance(data[field], str):
                errors.append(f"Field {field} must be a string")
    
    return errors


@predict_bp.route('/predict', methods=['POST'])
def predict():
    """
    Fraud prediction endpoint.
    
    Request body matches Course 3's api-contract.yaml schema.
    Response matches Course 3's model-card.md output format.
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body required'}), 400
    
    # Validate against Course 3's feature_schema.yaml
    validation_errors = validate_features(data)
    if validation_errors:
        return jsonify({
            'error': 'Validation failed',
            'details': validation_errors
        }), 400
    
    try:
        result = predictor.predict(data)
        return jsonify({
            'prediction': result['prediction'],
            'confidence': result['confidence'],
            'model_version': predictor.version,
            'features_used': result['features_used']
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Log the error in production
        return jsonify({'error': 'Prediction failed'}), 500
```

#### Context Boundary Visualization

```
┌──────────────────────────────────────────────────────────────┐
│                    /predict ENDPOINT                          │
│                                                               │
│   INPUT (API Context)              OUTPUT (API Context)       │
│   ───────────────────              ────────────────────       │
│   {                                {                          │
│     "amount": 1500.00,               "prediction": "fraud",   │
│     "merchant_category": "...",      "confidence": 0.87,      │
│     "time_since_last": 120           "model_version": "v1",   │
│   }                                  "features_used": [...]   │
│                                    }                          │
│                                                               │
│   ─────────────────── BOUNDARY ───────────────────────────   │
│                                                               │
│   HIDDEN (Service Context)                                    │
│   ────────────────────────                                    │
│   • Model weights (fraud_classifier_v1.pkl)                   │
│   • Feature engineering logic                                 │
│   • Prediction thresholds                                     │
│   • Internal metrics                                          │
└──────────────────────────────────────────────────────────────┘
```

> 💡 **Progressive Disclosure:** The `api-contract.yaml` from Course 3 IS the spec for this endpoint. The `api-advisor` agent reads it when answering questions about the /predict route. You don't need to memorize it.

> 🏢 **Enterprise Context:** Model serving has latency requirements:
> - **P50 latency:** Track median response time
> - **P99 latency:** Track worst-case for SLAs
> - **Model loading:** Load once at startup, not per-request
> - **Monitoring:** Add timing metrics in production

**Hands-On:**
- Create `src/routes/predict.py`
- Register blueprint in `app.py`
- Test with curl:
  ```bash
  curl -X POST http://localhost:5000/api/v1/predict \
    -H "Content-Type: application/json" \
    -d '{"amount": 1500.00, "merchant_category": "retail", "time_since_last": 120}'
  ```
- Verify response matches Course 3's expected format

[🎬 Video: Integrating Course 3's fraud model into /predict endpoint]

---

### 1.6 OpenAPI Spec-First Development (25 min)

**Concept:** Design the API contract before writing implementation code.

#### Why Spec-First?

| Code-First | Spec-First |
|------------|------------|
| Implementation drives design | Contract drives implementation |
| Documentation lags | Documentation IS the spec |
| Breaking changes discovered late | Breaking changes visible in spec diff |
| Hard to review API design | Review spec before any code |

#### Extending Course 3's API Contract

```yaml
# openapi/api-spec.yaml
openapi: 3.0.3
info:
  title: Fraud Detection API
  version: 1.0.0
  description: |
    API for fraud prediction and customer insights.
    
    ## Model Documentation
    See docs/model-card.md for model details.
    
    ## Course Context
    This API wraps Course 3's FraudPredictor and adds:
    - Customer management endpoints
    - AI-powered insights via Strands agents

servers:
  - url: http://localhost:5000/api/v1
    description: Local development

paths:
  /predict:
    post:
      summary: Predict fraud likelihood
      description: |
        Wraps Course 3's FraudPredictor.
        Input validated against feature_schema.yaml.
      operationId: predictFraud
      tags:
        - Predictions
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PredictRequest'
      responses:
        '200':
          description: Successful prediction
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PredictResponse'
        '400':
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
  
  /customers:
    get:
      summary: List customers
      operationId: listCustomers
      tags:
        - Customers
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 10
        - name: offset
          in: query
          schema:
            type: integer
            default: 0
      responses:
        '200':
          description: List of customers
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CustomerList'
    
    post:
      summary: Create a customer
      operationId: createCustomer
      tags:
        - Customers
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CustomerCreate'
      responses:
        '201':
          description: Customer created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Customer'
  
  /insights/{customer_id}:
    get:
      summary: Get AI-generated customer insights
      description: Uses Strands agent for analysis
      operationId: getCustomerInsights
      tags:
        - Insights
      parameters:
        - name: customer_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: AI-generated insights
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InsightsResponse'
        '404':
          description: Customer not found
        '504':
          description: Analysis timed out

components:
  schemas:
    PredictRequest:
      type: object
      required:
        - amount
        - merchant_category
      properties:
        amount:
          type: number
          description: Transaction amount
          example: 1500.00
        merchant_category:
          type: string
          description: Merchant category code
          example: "retail"
        time_since_last:
          type: integer
          description: Seconds since last transaction
          example: 120
    
    PredictResponse:
      type: object
      properties:
        prediction:
          type: string
          enum: [fraud, legitimate]
        confidence:
          type: number
          minimum: 0
          maximum: 1
        model_version:
          type: string
        features_used:
          type: array
          items:
            type: string
    
    Customer:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string
          format: email
    
    CustomerCreate:
      type: object
      required:
        - name
        - email
      properties:
        name:
          type: string
        email:
          type: string
          format: email
    
    CustomerList:
      type: object
      properties:
        customers:
          type: array
          items:
            $ref: '#/components/schemas/Customer'
        total:
          type: integer
        limit:
          type: integer
        offset:
          type: integer
    
    InsightsResponse:
      type: object
      properties:
        customer_id:
          type: integer
        insights:
          type: string
          description: AI-generated analysis
        model:
          type: string
          description: Model used for generation
    
    ErrorResponse:
      type: object
      properties:
        error:
          type: string
        details:
          type: array
          items:
            type: string
```

> 💡 **Progressive Disclosure:** The `schema-validator` agent validates your implementation against this spec. You don't manually check compliance — the gate agent does.

#### DARE Model Application

| Letter | Application in This Module |
|--------|---------------------------|
| **D** | OpenAPI validation is deterministic — use `make lint-openapi` |
| **A** | Agent helps draft endpoint descriptions |
| **R** | Review spec before implementation |
| **E** | If spec validation fails, fix spec or implementation |

**Hands-On:**
- Create `openapi/api-spec.yaml`
- Run `make lint-openapi` to validate
- View spec in Swagger UI: `make swagger-ui`

[📸 Screenshot: OpenAPI spec in Swagger UI]

---

### Module 1 Checkpoint

**By end of Module 1, you have:**
- ✅ Course 3 artifacts imported and verified
- ✅ Development environment configured
- ✅ Understanding of APIs as context boundaries
- ✅ `/predict` endpoint wrapping Course 3's model
- ✅ OpenAPI spec drafted and validated

**Git tag:** `module-1-setup`

**HISTORY.md Entry:**
```markdown
## Module 1 Complete

### Artifacts Imported from Course 3
- fraud_classifier_v1.pkl loaded successfully
- FraudPredictor class verified
- api-contract.yaml extended to api-spec.yaml
- feature_schema.yaml used for validation

### Decisions
- Using Flask (patterns transfer to FastAPI)
- SQLite for local development
- OpenAPI spec-first approach
- Model loaded once at startup (not per-request)

### Implementation
- /predict endpoint wrapping FraudPredictor
- Input validation against feature_schema.yaml

### Next: Module 2 — Flask Fundamentals
```

---

