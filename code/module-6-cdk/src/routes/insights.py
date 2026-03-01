"""
AI-Powered Customer Insights Endpoint.

Uses Strands agent for analysis with timeout handling.
"""

from flask import Blueprint, jsonify
from src.database.db import get_connection
from src.agents.customer_insights import get_insights_agent
import signal
import uuid

insights_bp = Blueprint('insights', __name__)

AGENT_TIMEOUT = 30


class AgentTimeoutError(Exception):
    pass


def _timeout_handler(signum, frame):
    raise AgentTimeoutError()


@insights_bp.route('/insights/<int:customer_id>', methods=['GET'])
def get_insights(customer_id: int):
    """Get AI-generated customer insights."""
    # DARE: Deterministic check first
    with get_connection() as conn:
        customer = conn.execute(
            'SELECT id, name FROM customers WHERE id = ?',
            (customer_id,)
        ).fetchone()

        if not customer:
            return jsonify({
                'error': 'Customer not found',
                'request_id': str(uuid.uuid4())[:8]
            }), 404

    # DARE: AI for ambiguity
    try:
        original_handler = signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(AGENT_TIMEOUT)

        try:
            agent = get_insights_agent()
            response = agent.run(f"Analyze customer {customer_id}")

            return jsonify({
                'customer_id': customer_id,
                'customer_name': customer['name'],
                'insights': response.content,
                'model': agent.model
            }), 200

        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, original_handler)

    except AgentTimeoutError:
        return jsonify({
            'error': 'Analysis timed out',
            'request_id': str(uuid.uuid4())[:8]
        }), 504

    except Exception:
        return jsonify({
            'error': 'Analysis failed',
            'request_id': str(uuid.uuid4())[:8]
        }), 500
