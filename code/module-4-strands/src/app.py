"""
Flask Application Factory.

Usage:
    from src.app import create_app
    app = create_app()
    app.run()
"""

from flask import Flask
import os


def create_app(config: dict = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    app.config.update(
        DATABASE_PATH=os.getenv('DATABASE_PATH', 'data/app.db'),
        MODEL_PATH=os.getenv('MODEL_PATH', 'models/fraud_classifier_v1.pkl'),
    )

    if config:
        app.config.update(config)

    # Register blueprints
    from src.routes.health import health_bp
    from src.routes.predict import predict_bp
    from src.routes.customers import customers_bp
    from src.routes.insights import insights_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(predict_bp, url_prefix='/api/v1')
    app.register_blueprint(customers_bp, url_prefix='/api/v1')
    app.register_blueprint(insights_bp, url_prefix='/api/v1')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
