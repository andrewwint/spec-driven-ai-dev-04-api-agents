"""Tests for Health endpoint."""

import pytest
from src.app import create_app


@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    return app.test_client()


class TestHealthEndpoint:

    def test_health_returns_200(self, client):
        response = client.get('/health')
        assert response.status_code == 200

    def test_health_returns_healthy(self, client):
        response = client.get('/health')
        data = response.get_json()
        assert data['status'] == 'healthy'

    def test_health_includes_version(self, client):
        response = client.get('/health')
        data = response.get_json()
        assert 'version' in data
