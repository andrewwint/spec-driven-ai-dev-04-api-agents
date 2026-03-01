## Module 4: Strands Agents (1.5 hrs)

### Learning Objectives
- Understand AI agents in API context
- Build a Strands agent for customer insights
- Create the `/insights` endpoint
- Set up the `strands-builder` agent

---

### 4.1 Why Agents in APIs? (20 min)

**Concept:** Understand when and why to add AI agents to your API.

#### When to Use Agents

| Use Agents For | Don't Use Agents For |
|----------------|---------------------|
| Natural language queries | Structured data lookups |
| Summarization/analysis | Simple CRUD operations |
| Multi-step reasoning | Deterministic calculations |
| Personalized responses | Batch processing |
| Ambiguous inputs | Clear, structured inputs |

#### The Customer Insights Use Case

```
┌────────────────────────────────────────────────────────────┐
│              /insights/{customer_id} ENDPOINT               │
│                                                             │
│   Human Question                     Agent Response         │
│   ──────────────                     ──────────────         │
│   "What's this customer's           "Customer Alice has    │
│    risk profile?"                    made 3 transactions   │
│                                      in the last month,    │
│                                      with 1 flagged as     │
│                                      potential fraud.      │
│                                      Risk level: MEDIUM."  │
│                                                             │
│   Why agent works here:                                     │
│   • Natural language output                                 │
│   • Synthesizes multiple data points                        │
│   • Provides contextual interpretation                      │
│   • Judgment about risk level                               │
└────────────────────────────────────────────────────────────┘
```

> 🏢 **Enterprise Context:** Agent calls cost money and add latency. Use them when the value justifies the cost:
> - **Claude Haiku:** ~$0.25 per 1M input tokens
> - **Claude Sonnet:** ~$3.00 per 1M input tokens
> - **Latency:** 1-5 seconds typical for agent response
>
> A `/customers` list endpoint should NOT use an agent — a database query is 100x faster and essentially free.

#### DARE Model Application

| Letter | Application in Agent Endpoints |
|--------|-------------------------------|
| **D** | Request validation, customer lookup — deterministic |
| **A** | Insight generation — requires AI reasoning |
| **R** | Human reviews agent outputs (in development) |
| **E** | Timeout handling, fallback responses |

---

### 4.2 Strands Agents Introduction (25 min)

**Concept:** Build a model-agnostic AI agent with Strands.

#### Why Strands?

| Factor | Strands | LangChain |
|--------|---------|-----------|
| **Model support** | Agnostic (any provider) | Historically OpenAI-focused |
| **Complexity** | Simpler API | Feature-rich but complex |
| **Learning curve** | Shallow | Steep |
| **Production ready** | Good | Good |
| **Community** | Growing | Large |

**Key Point:** Concepts transfer. Learn Strands → understand LangChain in a day.

#### Basic Strands Agent

```python
# src/skills/customer_insights.py
"""
Customer Insights Agent.

Uses Strands to generate AI-powered customer analysis.
Model-agnostic: can use Anthropic, OpenAI, or local models.
"""

from strands import Agent, tool
from src.database.db import get_connection
from typing import List, Dict, Any
import os


# Tools the agent can use
@tool
def get_customer_info(customer_id: int) -> Dict[str, Any]:
    """
    Get basic customer information.
    
    Args:
        customer_id: The customer's ID
        
    Returns:
        Customer info dict or error message
    """
    with get_connection() as conn:
        row = conn.execute(
            'SELECT * FROM customers WHERE id = ?',
            (customer_id,)
        ).fetchone()
        
        if not row:
            return {"error": f"Customer {customer_id} not found"}
        
        return {
            "id": row['id'],
            "name": row['name'],
            "email": row['email']
        }


@tool
def get_prediction_history(customer_id: int, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get customer's recent prediction history.
    
    Args:
        customer_id: The customer's ID
        limit: Max number of predictions to return
        
    Returns:
        List of prediction records
    """
    with get_connection() as conn:
        cursor = conn.execute('''
            SELECT prediction, confidence, created_at
            FROM predictions 
            WHERE customer_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (customer_id, limit))
        
        return [
            {
                "prediction": row['prediction'],
                "confidence": row['confidence'],
                "date": row['created_at']
            }
            for row in cursor.fetchall()
        ]


@tool
def get_fraud_statistics(customer_id: int) -> Dict[str, Any]:
    """
    Calculate fraud statistics for a customer.
    
    Args:
        customer_id: The customer's ID
        
    Returns:
        Statistics about fraud predictions
    """
    with get_connection() as conn:
        cursor = conn.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN prediction = 'fraud' THEN 1 ELSE 0 END) as fraud_count,
                AVG(confidence) as avg_confidence
            FROM predictions 
            WHERE customer_id = ?
        ''', (customer_id,))
        
        row = cursor.fetchone()
        
        total = row['total'] or 0
        fraud_count = row['fraud_count'] or 0
        
        return {
            "total_predictions": total,
            "fraud_count": fraud_count,
            "fraud_rate": fraud_count / total if total > 0 else 0,
            "average_confidence": row['avg_confidence'] or 0
        }


# Agent definition
def create_insights_agent():
    """
    Create the customer insights agent.
    
    Model selection:
    - Default: Claude Haiku (cheapest)
    - Override via INSIGHTS_MODEL env var
    """
    model = os.getenv('INSIGHTS_MODEL', 'anthropic/claude-3-haiku-20240307')
    
    return Agent(
        name="customer-insights",
        model=model,
        system_prompt="""You are a customer insights analyst for a fraud detection system.

Your job is to analyze customer data and provide clear, actionable insights.

When analyzing a customer:
1. First, get their basic info using get_customer_info
2. Get their prediction history using get_prediction_history
3. Get their fraud statistics using get_fraud_statistics
4. Synthesize the data into a clear analysis

Your analysis should include:
- Risk assessment (LOW / MEDIUM / HIGH)
- Key patterns observed
- Recommended actions (if any)

Be concise and factual. Do not make up data — only use what the tools return.
If a customer has no history, say so clearly.""",
        tools=[get_customer_info, get_prediction_history, get_fraud_statistics]
    )


# Singleton for reuse
_insights_agent = None

def get_insights_agent():
    """Get or create the insights agent (singleton)."""
    global _insights_agent
    if _insights_agent is None:
        _insights_agent = create_insights_agent()
    return _insights_agent
```

> 💡 **Progressive Disclosure:** Strands lets you swap models with one config change. Start with Haiku (cheap/fast), upgrade to Sonnet if quality isn't sufficient.

**Hands-On:**
- Create `src/skills/customer_insights.py`
- Set `ANTHROPIC_API_KEY` environment variable
- Test agent in Python REPL:
  ```python
  from src.agents.customer_insights import get_insights_agent
  agent = get_insights_agent()
  response = agent.run("Analyze customer 1")
  print(response.content)
  ```

---

### 4.3 The Insights Endpoint (25 min)

**Concept:** Wrap the Strands agent in a Flask endpoint.

#### Endpoint Implementation

```python
# src/routes/insights.py
"""
AI-powered customer insights endpoint.

Uses Strands agent for analysis.
Includes timeout handling and fallback behavior.
"""

from flask import Blueprint
from src.agents.customer_insights import get_insights_agent
from src.database.db import get_connection
from src.utils.responses import success_response, error_response
import signal

insights_bp = Blueprint('insights', __name__)

# Timeout for agent calls (seconds)
AGENT_TIMEOUT = 30


class TimeoutError(Exception):
    """Raised when agent call times out."""
    pass


def timeout_handler(signum, frame):
    raise TimeoutError("Agent analysis timed out")


@insights_bp.route('/insights/<int:customer_id>', methods=['GET'])
def get_insights(customer_id: int):
    """
    Get AI-generated insights for a customer.
    
    Uses Strands agent for analysis.
    Returns 504 if analysis times out.
    """
    # DARE: Deterministic check first
    with get_connection() as conn:
        customer = conn.execute(
            'SELECT id, name FROM customers WHERE id = ?',
            (customer_id,)
        ).fetchone()
        
        if not customer:
            return error_response('Customer not found', 404)
    
    # DARE: AI for Ambiguity
    try:
        # Set timeout
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(AGENT_TIMEOUT)
        
        try:
            agent = get_insights_agent()
            response = agent.run(f"Analyze customer {customer_id}")
            
            return success_response({
                'customer_id': customer_id,
                'customer_name': customer['name'],
                'insights': response.content,
                'model': agent.model
            })
            
        finally:
            # Cancel timeout
            signal.alarm(0)
    
    except TimeoutError:
        # DARE: Escalate on Failure
        return error_response(
            'Analysis timed out',
            504,
            details=[
                f'Agent did not respond within {AGENT_TIMEOUT} seconds',
                'Please try again or contact support'
            ]
        )
    
    except Exception as e:
        # Log error in production
        return error_response(
            'Analysis failed',
            500,
            details=['An unexpected error occurred']
        )
```

#### Context Boundary for Agent Endpoint

```
┌────────────────────────────────────────────────────────────────┐
│                  AGENT ENDPOINT CONTEXT                         │
│                                                                 │
│   API Layer           Agent Layer           External Services   │
│   ─────────           ───────────           ─────────────────   │
│                                                                 │
│   customer_id  ──►    Agent prompt   ──►    LLM API call       │
│                       + tool calls          (Claude/GPT/etc)   │
│                       + tool results                            │
│                                                                 │
│                       Agent sees:           Agent DOESN'T see:  │
│                       • Customer ID         • API auth tokens   │
│                       • Tool results        • Other customers   │
│                       • System prompt       • Internal configs  │
│                       • Its own tools       • Database directly │
│                                                                 │
│   Response    ◄──    Agent output    ◄──    LLM response       │
└────────────────────────────────────────────────────────────────┘
```

> 🏢 **Enterprise Context:** Agent timeouts are critical:
> - **User experience:** 30 seconds is a long wait
> - **API Gateway limits:** AWS API Gateway has 29-second timeout
> - **Cost control:** Runaway agents waste money
> - **Always have fallbacks:** What happens when the LLM is down?

**Hands-On:**
- Create `src/routes/insights.py`
- Register blueprint in `app.py`
- Test with curl:
  ```bash
  curl http://localhost:5000/api/v1/insights/1
  ```
- Intentionally set `AGENT_TIMEOUT=1` to trigger timeout handling

[🎬 Video: Testing insights endpoint with real agent call]

---

### 4.4 The Strands-Builder Agent (20 min)

**Concept:** Set up a Doer agent that creates Strands agents following project patterns.

#### Agent Definition

```yaml
# .github/skills/strands-builder/SKILL.md
---
name: strands-builder
description: Creates Strands agents following project patterns
tools:
  - read
  - edit
  - terminal
  - mcp:strands-agents
model_tier: balanced  # Building agents requires nuanced reasoning
---

# Strands Builder Agent

## Role
Create new Strands agents that integrate with the API.
Each agent should have a clear purpose, appropriate tools, and proper error handling.

## Process
1. Understand the use case from human
2. Use MCP to fetch Strands documentation for current patterns
3. Check existing agents in `src/skills/` for project conventions
4. Design tools the agent needs
5. Create agent with system prompt
6. Create corresponding Flask endpoint in `src/routes/`
7. Hand off to reviewer for quality check

## Restrictions
- Cannot modify existing agents without explicit approval
- Must use cheapest model that works (default: Haiku)
- Must include timeout handling in endpoints
- Tools must use existing database patterns (get_connection)

## Model Selection Guidelines

| Use Case | Model | Why |
|----------|-------|-----|
| Simple analysis | claude-3-haiku | Cheap, fast |
| Complex reasoning | claude-3-sonnet | Better judgment |
| Production default | claude-3-haiku | Cost control |

## Handoffs
- Receives from: Human (use case), api-advisor (architectural guidance)
- Hands off to: reviewer (for quality check)

## MCP Usage
When unsure about Strands patterns:
1. Use `mcp:strands-agents` server
2. Search for relevant documentation
3. Follow official patterns in implementation

## Progressive Disclosure Hints

| Topic | Action |
|-------|--------|
| Strands syntax | Use strands-agents MCP server |
| Tool creation | Check `src/skills/customer_insights.py` for patterns |
| Database access | Use `get_connection()` from `src/database/db.py` |
| Error handling | Follow timeout pattern in `src/routes/insights.py` |
| Model selection | Start with Haiku, upgrade if quality insufficient |

## Example: Creating a Transaction Summarizer Agent

Human asks: "Create an agent that summarizes transaction patterns"

1. Search Strands MCP: "agent tools database"
2. Check existing: `src/skills/customer_insights.py`
3. Design tools:
   - `get_recent_transactions(days: int)`
   - `calculate_spending_summary()`
4. Create agent with summary-focused prompt
5. Create `/transactions/summary` endpoint
6. Report: "Created transaction_summarizer.py, ready for review"
```

**Hands-On:**
- Create `.github/skills/strands-builder/SKILL.md`
- Ask agent to create a "transaction summarizer" agent
- Review generated code for:
  - Appropriate model selection (Haiku)
  - Timeout handling
  - Database patterns match existing code

---

### Module 4 Checkpoint

**By end of Module 4, you have:**
- ✅ Strands agent for customer insights
- ✅ `/insights` endpoint with timeout handling
- ✅ `strands-builder` agent for creating new agents
- ✅ Understanding of when to use agents vs. simple queries

**Git tag:** `module-4-strands`

**HISTORY.md Entry:**
```markdown
## Module 4 Complete

### Implemented
- customer_insights_agent with 3 tools:
  - get_customer_info
  - get_prediction_history
  - get_fraud_statistics
- /insights/{customer_id} endpoint
- Timeout handling (30 seconds) with 504 fallback

### Decisions
- Using Claude Haiku for cost efficiency (~$0.25/1M tokens)
- 30-second timeout for agent calls
- Deterministic validation before agent invocation (DARE)
- Singleton pattern for agent reuse

### Agent Activity
- strands-builder created transaction-summarizer agent

### Next: Module 5 — MCP "10x Google Fu" ⭐
```

---

