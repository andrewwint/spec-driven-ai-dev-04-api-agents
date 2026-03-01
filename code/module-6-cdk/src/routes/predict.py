"""
Fraud Prediction Endpoint.

Wraps Course 3's FraudPredictor in a Flask endpoint.
"""

from flask import Blueprint, request, jsonify
import os
import uuid

predict_bp = Blueprint('predict', __name__)

_predictor = None


def get_predictor():
    """Get or create FraudPredictor (singleton)."""
    global _predictor
    if _predictor is None:
        from src.ml.predict import FraudPredictor
        model_path = os.getenv('MODEL_PATH', 'models/fraud_classifier_v1.pkl')
        _predictor = FraudPredictor(model_path)
    return _predictor


@predict_bp.route('/predict', methods=['POST'])
def predict():
    """Fraud prediction endpoint."""
    data = request.get_json()

    if not data:
        return jsonify({
            'error': 'Request body required',
            'request_id': str(uuid.uuid4())[:8]
        }), 400

    try:
        predictor = get_predictor()
        errors = predictor.validate(data)

        if errors:
            return jsonify({
                'error': 'Validation failed',
                'details': errors,
                'request_id': str(uuid.uuid4())[:8]
            }), 400

        result = predictor.predict(data)
        return jsonify(result), 200

    except FileNotFoundError as e:
        return jsonify({
            'error': 'Model not available',
            'details': [str(e)],
            'request_id': str(uuid.uuid4())[:8]
        }), 503

    except Exception:
        return jsonify({
            'error': 'Prediction failed',
            'request_id': str(uuid.uuid4())[:8]
        }), 500
