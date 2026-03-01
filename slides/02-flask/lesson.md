## Module 2: Flask Fundamentals (1.5 hrs)

### Learning Objectives
- Build Flask routes that follow the OpenAPI spec
- Use blueprints for code organization
- Set up the `endpoint-generator` agent
- Implement request/response handling patterns

---

### 2.1 Flask Application Structure (25 min)

**Concept:** Organize Flask applications for maintainability and agent-assisted development.

#### Application Factory Pattern

```python
# src/app.py
"""
Flask application factory.

Uses the factory pattern for:
- Testability (create app with test config)
- Modularity (blueprints registered separately)
- Agent-friendliness (agents work on one blueprint at a time)
"""

from flask import Flask
import os


def create_app(config=None):
    """
    Application factory pattern.
    
    Args:
        config: Optional dict of configuration overrides
    
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Default configuration
    app.config.update(
        DATABASE_PATH=os.getenv('DATABASE_PATH', 'data/app.db'),
        MODEL_PATH=os.getenv('MODEL_PATH', 'models/fraud_classifier_v1.pkl'),
    )
    
    # Override with provided config
    if config:
        app.config.update(config)
    
    # Initialize database
    from src.database.db import init_db
    with app.app_context():
        init_db()
    
    # Register blueprints
    from src.routes.predict import predict_bp
    from src.routes.customers import customers_bp
    from src.routes.insights import insights_bp
    
    app.register_blueprint(predict_bp, url_prefix='/api/v1')
    app.register_blueprint(customers_bp, url_prefix='/api/v1')
    app.register_blueprint(insights_bp, url_prefix='/api/v1')
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    return app


# Development server entry point
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
```

#### Why This Structure?

| Benefit | How It Helps |
|---------|--------------|
| **Testability** | Create app with test config |
| **Modularity** | Each blueprint is independent |
| **Agent-friendly** | Agents work on one blueprint at a time |
| **Scalability** | Easy to split into microservices later |

> 💡 **Progressive Disclosure:** The `endpoint-generator` agent creates new routes as blueprints. It reads existing blueprints to match conventions — this is "discovered" context.

**Hands-On:**
- Create `src/app.py` with factory pattern
- Run `flask run` to verify startup
- Access health endpoint: `curl http://localhost:5000/health`

---

### 2.2 The Endpoint-Generator Agent (25 min)

**Concept:** Set up a Doer agent that creates Flask routes following project conventions.

#### Agent Definition

```yaml
# .github/skills/endpoint-generator/SKILL.md
---
name: endpoint-generator
description: Creates Flask routes following project conventions
tools:
  - read
  - edit
  - terminal
model_tier: fast  # Structured task, clear inputs
---

# Endpoint Generator Agent

## Role
Create new Flask endpoints that follow existing patterns.
Do NOT improvise — match the conventions in existing routes.

## Process
1. Read `openapi/api-spec.yaml` for endpoint contract
2. Read existing routes in `src/routes/` for conventions
3. Generate new route blueprint
4. Run `make lint` to verify syntax
5. Hand off to schema-validator for compliance check

## Restrictions
- Only creates routes defined in OpenAPI spec
- Cannot modify `src/ml/` (model code is from Course 3)
- Cannot modify `openapi/api-spec.yaml` (spec is authoritative)
- Must use existing patterns from `src/routes/`

## Handoffs
- Receives from: Human (with spec), api-advisor (with guidance)
- Hands off to: schema-validator (for compliance check)

## Progressive Disclosure Hints

| Topic | Action |
|-------|--------|
| Request validation | Check `docs/feature_schema.yaml` |
| Response format | Read existing routes for patterns |
| Error handling | Follow patterns in `src/routes/predict.py` |
| Blueprint naming | Match `{resource}_bp` convention |

## Example Generation

When asked to create `/customers` GET endpoint:

1. Read `openapi/api-spec.yaml` → find `/customers` GET spec
2. Read `src/routes/predict.py` → note patterns
3. Generate:

```python
# src/routes/customers.py
from flask import Blueprint, request, jsonify
from src.database.db import get_connection
from src.models.customer import CustomerDTO

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/customers', methods=['GET'])
def list_customers():
    """List customers with pagination."""
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    with get_connection() as conn:
        # ... implementation
```

4. Run `make lint`
5. Report: "Created customers.py, ready for schema-validator review"
```

#### DARE Model Application

| Letter | Application |
|--------|-------------|
| **D** | `make lint` validates Python syntax — deterministic |
| **A** | Agent generates route code — ambiguous task |
| **R** | Human reviews generated routes before merge |
| **E** | If generation fails spec validation, human intervenes |

**Hands-On:**
- Create `.github/skills/endpoint-generator/SKILL.md`
- Ask agent to create `/customers` GET endpoint
- Review generated code
- Run `make lint` to verify

---

### 2.3 Request/Response Handling (20 min)

**Concept:** Handle API inputs and outputs following the OpenAPI spec.

#### Consistent Error Response Pattern

```python
# src/utils/responses.py
"""Consistent response helpers."""

from flask import jsonify
from typing import List, Optional
import uuid


def success_response(data: dict, status: int = 200):
    """Standard success response."""
    return jsonify(data), status


def error_response(
    message: str, 
    status: int = 400, 
    details: Optional[List[str]] = None
):
    """
    Standard error response.
    
    Consistent format across all endpoints:
    - error: Human-readable message
    - details: List of specific issues
    - request_id: For debugging/support
    """
    response = {
        'error': message,
        'request_id': str(uuid.uuid4())[:8]  # Short ID for support
    }
    
    if details:
        response['details'] = details
    
    return jsonify(response), status


def validation_error(errors: List[str]):
    """Shorthand for validation errors."""
    return error_response(
        message='Validation failed',
        status=400,
        details=errors
    )
```

#### Using Response Helpers

```python
# In routes
from src.utils.responses import success_response, error_response, validation_error

@customers_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id: int):
    customer = find_customer(customer_id)
    
    if not customer:
        return error_response('Customer not found', 404)
    
    return success_response(customer.to_dict())
```

> 🏢 **Enterprise Context:** Consistent error formats matter for:
> - **Client development:** Predictable error handling
> - **Debugging:** Request IDs link logs to errors
> - **Monitoring:** Structured errors enable alerts
> - **API versioning:** Error format is part of your contract

---

### 2.4 Blueprint Organization (20 min)

**Concept:** Organize routes into logical blueprints.

#### Blueprint Structure

```
src/routes/
├── __init__.py
├── predict.py      # /predict - Course 3 model integration
├── customers.py    # /customers - CRUD operations
└── insights.py     # /insights - Strands agent (Module 4)
```

#### Customers Blueprint

```python
# src/routes/customers.py
"""
Customer management endpoints.
CRUD operations with SQLite backend.
"""

from flask import Blueprint, request
from src.database.db import get_connection
from src.models.customer import CustomerDTO, CustomerCreateDTO
from src.utils.responses import success_response, error_response, validation_error

customers_bp = Blueprint('customers', __name__)


@customers_bp.route('/customers', methods=['GET'])
def list_customers():
    """
    List customers with pagination.
    
    Query params:
        limit: Max results (default 10)
        offset: Skip first N results (default 0)
    """
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    # Validate pagination params
    if limit < 1 or limit > 100:
        return validation_error(['limit must be between 1 and 100'])
    if offset < 0:
        return validation_error(['offset must be non-negative'])
    
    with get_connection() as conn:
        # Get total count
        total = conn.execute('SELECT COUNT(*) FROM customers').fetchone()[0]
        
        # Get paginated results
        cursor = conn.execute(
            'SELECT * FROM customers LIMIT ? OFFSET ?',
            (limit, offset)
        )
        customers = [CustomerDTO.from_db_row(row) for row in cursor.fetchall()]
    
    return success_response({
        'customers': [c.to_dict() for c in customers],
        'total': total,
        'limit': limit,
        'offset': offset
    })


@customers_bp.route('/customers', methods=['POST'])
def create_customer():
    """Create a new customer."""
    data = request.get_json()
    
    if not data:
        return error_response('Request body required', 400)
    
    try:
        customer_input = CustomerCreateDTO.from_request(data)
    except ValueError as e:
        return validation_error([str(e)])
    
    with get_connection() as conn:
        # Check for duplicate email
        existing = conn.execute(
            'SELECT id FROM customers WHERE email = ?',
            (customer_input.email,)
        ).fetchone()
        
        if existing:
            return error_response('Email already exists', 409)
        
        cursor = conn.execute(
            'INSERT INTO customers (name, email) VALUES (?, ?)',
            (customer_input.name, customer_input.email)
        )
        conn.commit()
        
        # Fetch created customer
        created = conn.execute(
            'SELECT * FROM customers WHERE id = ?',
            (cursor.lastrowid,)
        ).fetchone()
        
        customer = CustomerDTO.from_db_row(created)
    
    return success_response(customer.to_dict(), 201)


@customers_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id: int):
    """Get a specific customer by ID."""
    with get_connection() as conn:
        row = conn.execute(
            'SELECT * FROM customers WHERE id = ?',
            (customer_id,)
        ).fetchone()
        
        if not row:
            return error_response('Customer not found', 404)
        
        customer = CustomerDTO.from_db_row(row)
    
    return success_response(customer.to_dict())
```

---

### Module 2 Checkpoint

**By end of Module 2, you have:**
- ✅ Flask application with factory pattern
- ✅ Blueprint organization for routes
- ✅ `endpoint-generator` agent creating routes
- ✅ Consistent request/response handling

**Git tag:** `module-2-flask`

**HISTORY.md Entry:**
```markdown
## Module 2 Complete

### Implemented
- Application factory pattern in app.py
- Blueprint structure: predict, customers
- Consistent error response format
- endpoint-generator agent for route creation

### Patterns Established
- Blueprint naming: {resource}_bp
- Response helpers in src/utils/responses.py
- Pagination pattern for list endpoints

### Agent Activity
- endpoint-generator created /customers endpoints
- Verified OpenAPI compliance with schema-validator

### Next: Module 3 — Database Integration
```

---

