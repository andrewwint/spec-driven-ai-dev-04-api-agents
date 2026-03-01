"""
Customer Insights Agent.

Uses Strands for AI-powered customer analysis.
Model-agnostic: works with Anthropic, OpenAI, or local models.
"""

from strands import Agent, tool
from src.database.db import get_connection
from typing import List, Dict, Any
import os


@tool
def get_customer_info(customer_id: int) -> Dict[str, Any]:
    """Get basic customer information."""
    with get_connection() as conn:
        row = conn.execute(
            'SELECT id, name, email FROM customers WHERE id = ?',
            (customer_id,)
        ).fetchone()

        if not row:
            return {"error": f"Customer {customer_id} not found"}

        return {"id": row['id'], "name": row['name'], "email": row['email']}


@tool
def get_prediction_history(customer_id: int, limit: int = 10) -> List[Dict[str, Any]]:
    """Get customer's recent prediction history."""
    with get_connection() as conn:
        cursor = conn.execute('''
            SELECT prediction, confidence, created_at
            FROM predictions
            WHERE customer_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (customer_id, limit))

        return [
            {"prediction": row['prediction'], "confidence": float(row['confidence']), "date": row['created_at']}
            for row in cursor.fetchall()
        ]


@tool
def get_fraud_statistics(customer_id: int) -> Dict[str, Any]:
    """Calculate fraud statistics for a customer."""
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
            "fraud_rate": round(fraud_count / total, 3) if total > 0 else 0,
            "average_confidence": round(row['avg_confidence'] or 0, 3)
        }


def create_insights_agent() -> Agent:
    """Create the customer insights agent."""
    model = os.getenv('INSIGHTS_MODEL', 'anthropic/claude-3-haiku-20240307')

    return Agent(
        name="customer-insights",
        model=model,
        system_prompt="""You are a customer insights analyst for a fraud detection system.

When analyzing a customer:
1. Get their basic info using get_customer_info
2. Get their prediction history using get_prediction_history
3. Get their fraud statistics using get_fraud_statistics
4. Synthesize into a clear analysis

Include:
- Risk Assessment: LOW / MEDIUM / HIGH
- Key Patterns
- Recommendations

Be concise. Only use data from tools.""",
        tools=[get_customer_info, get_prediction_history, get_fraud_statistics]
    )


_insights_agent = None


def get_insights_agent() -> Agent:
    """Get or create the insights agent (singleton)."""
    global _insights_agent
    if _insights_agent is None:
        _insights_agent = create_insights_agent()
    return _insights_agent
