## Module 3: Database Integration (1.5 hrs)

### Learning Objectives
- Integrate SQLite for local development
- Build DTOs (Data Transfer Objects) for clean data handling
- Understand the cloud upgrade path (SQLite → PostgreSQL)
- Set up the `dto-builder` agent

---

### 3.1 SQLite for Local Development (25 min)

**Concept:** Use SQLite for zero-configuration local development with patterns that transfer to production databases.

#### Why SQLite First?

| Benefit | Description |
|---------|-------------|
| **Zero setup** | No server, no credentials, no Docker |
| **Portable** | Database is a single file |
| **Same SQL** | Queries transfer to PostgreSQL/MySQL |
| **Fast iteration** | Delete file to reset, no migrations needed |

#### Database Module

```python
# src/database/db.py
"""
Database connection and initialization.

Uses SQLite for local development.
Patterns transfer to PostgreSQL (see Cloud Upgrade Path section).
"""

import sqlite3
from contextlib import contextmanager
import os

DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/app.db')


@contextmanager
def get_connection():
    """
    Context manager for database connections.
    
    Usage:
        with get_connection() as conn:
            conn.execute('SELECT * FROM customers')
    
    Ensures connections are properly closed.
    """
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Dict-like access to rows
    
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """
    Initialize database schema.
    
    Safe to call multiple times (uses IF NOT EXISTS).
    """
    with get_connection() as conn:
        conn.executescript('''
            -- Customers table
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Predictions history
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER REFERENCES customers(id),
                prediction TEXT NOT NULL,
                confidence REAL NOT NULL,
                request_data TEXT,  -- JSON of input features
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Create indexes for common queries
            CREATE INDEX IF NOT EXISTS idx_predictions_customer 
                ON predictions(customer_id);
            CREATE INDEX IF NOT EXISTS idx_predictions_created 
                ON predictions(created_at);
        ''')
        conn.commit()


def reset_db():
    """Reset database (for testing)."""
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
    init_db()
```

> 💡 **Progressive Disclosure:** The connection manager pattern (`@contextmanager`) transfers directly to PostgreSQL with psycopg2. Module 3.3 shows the upgrade path.

**Hands-On:**
- Create `src/database/db.py`
- Create `data/` directory
- Run `init_db()` in Python REPL
- Verify tables exist: `sqlite3 data/app.db ".tables"`

---

### 3.2 DTOs — Data Transfer Objects (25 min)

**Concept:** Use DTOs to separate API representation from database schema.

#### Why DTOs?

| Without DTOs | With DTOs |
|--------------|-----------|
| Database schema exposed to API | Clean separation of concerns |
| Changing DB breaks API | Change DB without breaking API |
| All fields always returned | Control what crosses the boundary |
| Validation scattered | Validation centralized in DTO |

#### Customer DTOs

```python
# src/models/customer.py
"""
Customer Data Transfer Objects.

DTOs define:
- What crosses the API boundary (to_dict)
- How to create from database rows (from_db_row)
- How to validate input (from_request)
"""

from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class CustomerDTO:
    """API representation of a customer."""
    id: int
    name: str
    email: str
    
    @classmethod
    def from_db_row(cls, row):
        """
        Convert database row to DTO.
        
        Note: row is sqlite3.Row with dict-like access.
        """
        return cls(
            id=row['id'],
            name=row['name'],
            email=row['email']
            # Note: created_at is NOT exposed to API
        )
    
    def to_dict(self):
        """Convert to JSON-serializable dict."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


@dataclass
class CustomerCreateDTO:
    """Input for creating a customer."""
    name: str
    email: str
    
    @classmethod
    def from_request(cls, data: dict):
        """
        Validate and create from request data.
        
        Raises:
            ValueError: If validation fails
        """
        errors = []
        
        # Validate name
        name = data.get('name', '').strip()
        if not name:
            errors.append('name is required')
        elif len(name) > 100:
            errors.append('name must be 100 characters or less')
        
        # Validate email
        email = data.get('email', '').strip().lower()
        if not email:
            errors.append('email is required')
        elif not cls._is_valid_email(email):
            errors.append('email format is invalid')
        
        if errors:
            raise ValueError('; '.join(errors))
        
        return cls(name=name, email=email)
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Basic email validation."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))


@dataclass 
class PredictionDTO:
    """API representation of a prediction."""
    id: int
    customer_id: Optional[int]
    prediction: str
    confidence: float
    
    @classmethod
    def from_db_row(cls, row):
        return cls(
            id=row['id'],
            customer_id=row['customer_id'],
            prediction=row['prediction'],
            confidence=row['confidence']
            # Note: request_data and created_at NOT exposed
        )
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'prediction': self.prediction,
            'confidence': self.confidence
        }
```

#### Context Boundary Visualization

```
┌────────────────────────────────────────────────────────────┐
│                 DTO AS CONTEXT BOUNDARY                     │
│                                                             │
│   Database Row              DTO                  API JSON   │
│   ────────────              ───                  ────────   │
│   id: 1                     id: 1                "id": 1    │
│   name: "Alice"      →      name: "Alice"   →    "name": "Alice"
│   email: "a@b.com"          email: "a@b.com"     "email": "a@b.com"
│   created_at: ...           (not included)       (not in response)
│                                                             │
│   Database stores more      DTO selects what    API sees   │
│   than API should expose    crosses boundary    only DTO   │
└────────────────────────────────────────────────────────────┘
```

> 🏢 **Enterprise Context:** DTOs are essential for:
> - **API versioning:** Old clients get v1 DTO, new clients get v2 DTO
> - **Security:** Never accidentally expose internal fields (like internal_score)
> - **Performance:** Only serialize what's needed
> - **Documentation:** DTOs self-document the API contract

**Hands-On:**
- Create `src/models/customer.py` with DTOs
- Update `/customers` endpoint to use DTOs
- Test that `created_at` doesn't appear in API response

---

### 3.3 The Cloud Upgrade Path (20 min)

**Concept:** Understand how SQLite patterns transfer to production databases.

#### SQLite → PostgreSQL Migration Path

```python
# src/database/db.py — After migration to PostgreSQL

"""
Database connection with environment-based configuration.

Supports both SQLite (local) and PostgreSQL (production).
Switch via DATABASE_URL environment variable.
"""

import os
from contextlib import contextmanager
from urllib.parse import urlparse

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/app.db')


def get_db_type():
    """Determine database type from URL."""
    if DATABASE_URL.startswith('sqlite'):
        return 'sqlite'
    elif DATABASE_URL.startswith('postgres'):
        return 'postgresql'
    else:
        raise ValueError(f"Unsupported database: {DATABASE_URL}")


@contextmanager
def get_connection():
    """
    Get database connection.
    
    Works with both SQLite and PostgreSQL.
    The connection interface is compatible.
    """
    db_type = get_db_type()
    
    if db_type == 'sqlite':
        import sqlite3
        path = DATABASE_URL.replace('sqlite:///', '')
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
    
    elif db_type == 'postgresql':
        import psycopg2
        from psycopg2.extras import RealDictCursor
        
        parsed = urlparse(DATABASE_URL)
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            user=parsed.username,
            password=parsed.password,
            database=parsed.path[1:],  # Remove leading /
            cursor_factory=RealDictCursor
        )
    
    try:
        yield conn
    finally:
        conn.close()
```

#### What Changes, What Stays

| Aspect | SQLite | PostgreSQL | Code Change |
|--------|--------|------------|-------------|
| Connection string | File path | URL | Config only |
| SQL syntax | Standard | Standard | Almost none |
| Transactions | Implicit | Explicit | Minor |
| Connection pooling | Not needed | Essential | Add pool |
| Migrations | Manual | Alembic | Add tool |

> 💡 **Progressive Disclosure:** Course 5 implements the full migration with RDS, connection pooling, and Alembic migrations. Here we just understand the path exists.

#### ROI Trade-off: Database Choice

| Factor | SQLite | PostgreSQL |
|--------|--------|------------|
| **Setup time** | 0 min | 30+ min |
| **Monthly cost** | $0 | $15-50+ minimum |
| **Concurrency** | Limited (write locks) | Excellent |
| **Features** | Basic SQL | JSONB, full-text, etc. |
| **Ops burden** | None | Backups, monitoring |

**Decision Framework:**
- **Solo dev / MVP:** SQLite until you hit limits
- **Team / Production:** PostgreSQL from the start
- **Learning:** SQLite — patterns transfer anyway
- **When to migrate:** >10 concurrent users, or need PostgreSQL features

---

### 3.4 The DTO-Builder Agent (20 min)

**Concept:** Set up a Doer agent that creates DTOs from OpenAPI schemas.

#### Agent Definition

```yaml
# .github/skills/dto-builder/SKILL.md
---
name: dto-builder
description: Creates DTOs from OpenAPI schemas
tools:
  - read
  - edit
model_tier: fast  # Schema → DTO is mechanical transformation
---

# DTO Builder Agent

## Role
Create data transfer objects that match OpenAPI component schemas.
DTOs are the context boundary between database and API.

## Process
1. Read `openapi/api-spec.yaml` for schema definitions
2. Read existing DTOs in `src/models/` for patterns
3. Create DTO class with:
   - `from_db_row()` - database → DTO
   - `to_dict()` - DTO → JSON
   - `from_request()` - JSON → DTO (for input DTOs)
4. Run `make lint` to verify

## Restrictions
- Cannot modify database schema (db.py)
- Cannot modify OpenAPI spec (spec is authoritative)
- DTOs must match schema exactly — no extra fields
- Validation logic only in input DTOs (CreateDTO, UpdateDTO)

## Handoffs
- Receives from: endpoint-generator (needs DTO for new route)
- Hands off to: schema-validator (verify compliance)

## Progressive Disclosure Hints

| Topic | Action |
|-------|--------|
| Schema types | Read `openapi/api-spec.yaml` components section |
| Validation rules | Check `docs/feature_schema.yaml` |
| Existing patterns | Read `src/models/customer.py` for conventions |
| Type mapping | OpenAPI string→str, number→float, integer→int |

## Example Generation

When asked to create `PredictionDTO`:

1. Read OpenAPI schema:
```yaml
PredictResponse:
  properties:
    prediction:
      type: string
      enum: [fraud, legitimate]
    confidence:
      type: number
```

2. Generate:
```python
@dataclass
class PredictionDTO:
    prediction: str  # "fraud" | "legitimate"
    confidence: float
    
    def to_dict(self):
        return {
            'prediction': self.prediction,
            'confidence': self.confidence
        }
```

3. Run `make lint`
4. Report: "Created PredictionDTO, ready for review"
```

**Hands-On:**
- Create `.github/skills/dto-builder/SKILL.md`
- Ask agent to create `PredictionHistoryDTO` from spec
- Review generated code

---

### Module 3 Checkpoint

**By end of Module 3, you have:**
- ✅ SQLite database with schema
- ✅ DTOs for clean data handling
- ✅ Cloud upgrade path documented
- ✅ `dto-builder` agent creating DTOs

**Git tag:** `module-3-database`

**HISTORY.md Entry:**
```markdown
## Module 3 Complete

### Implemented
- SQLite database in data/app.db
- CustomerDTO, CustomerCreateDTO, PredictionDTO
- Database connection manager with upgrade path

### Decisions
- SQLite for local dev (can migrate to PostgreSQL later)
- DTOs separate database from API representation
- Environment-based database URL configuration
- created_at not exposed in API (internal tracking only)

### Agent Activity
- dto-builder created PredictionDTO from OpenAPI schema
- Patterns established for future DTOs

### Next: Module 4 — Strands Agents
```

---

