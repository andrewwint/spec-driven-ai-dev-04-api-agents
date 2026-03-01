"""Health check endpoint."""

from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """Service health check."""
    return jsonify({'status': 'healthy', 'version': '1.0.0'}), 200
