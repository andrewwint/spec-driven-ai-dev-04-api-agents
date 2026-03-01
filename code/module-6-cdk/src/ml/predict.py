"""
Fraud Predictor - Course 3 Model Integration

Copy fraud_classifier_v1.pkl from Course 3 to models/ directory.

Usage:
    predictor = FraudPredictor('models/fraud_classifier_v1.pkl')
    result = predictor.predict({
        'amount': 150.00,
        'merchant_category': 'retail',
        'time_since_last': 3600
    })
"""

import joblib
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List
import os


class FraudPredictor:
    """Production prediction interface for fraud detection."""

    VALID_CATEGORIES = ['grocery', 'retail', 'restaurant', 'gas', 'travel',
                        'entertainment', 'healthcare', 'utilities', 'jewelry', 'electronics']

    def __init__(self, model_path: str = 'models/fraud_classifier_v1.pkl'):
        """Load model from path."""
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model not found: {model_path}. "
                "Copy fraud_classifier_v1.pkl from Course 3."
            )

        self.model = joblib.load(model_path)
        self.model_version = Path(model_path).stem

    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Make a fraud prediction."""
        errors = self.validate(features)
        if errors:
            raise ValueError("; ".join(errors))

        df = pd.DataFrame([{
            'amount': features['amount'],
            'merchant_category_encoded': self._encode_category(features['merchant_category']),
            'time_since_last': features.get('time_since_last', 0),
        }])

        prediction = int(self.model.predict(df)[0])
        probability = self.model.predict_proba(df)[0]

        return {
            'prediction': 'fraud' if prediction == 1 else 'legitimate',
            'confidence': float(max(probability)),
            'model_version': self.model_version,
            'features_used': list(features.keys())
        }

    def validate(self, features: Dict[str, Any]) -> List[str]:
        """Validate input features. Returns list of errors."""
        errors = []

        if 'amount' not in features:
            errors.append("Missing required feature: amount")
        elif not isinstance(features['amount'], (int, float)):
            errors.append("amount must be numeric")
        elif features['amount'] < 0:
            errors.append("amount must be non-negative")

        if 'merchant_category' not in features:
            errors.append("Missing required feature: merchant_category")
        elif not isinstance(features['merchant_category'], str):
            errors.append("merchant_category must be a string")

        return errors

    def _encode_category(self, category: str) -> int:
        """Encode merchant category to numeric."""
        category_map = {cat: i for i, cat in enumerate(self.VALID_CATEGORIES)}
        return category_map.get(category.lower(), hash(category) % 10)
