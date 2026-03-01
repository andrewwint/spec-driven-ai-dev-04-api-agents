"""Tests for Customer endpoints."""

import pytest
from src.app import create_app
from src.database.db import reset_db


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DATABASE_PATH': 'data/test.db'
    })
    with app.app_context():
        reset_db()
    return app


@pytest.fixture
def client(app):
    return app.test_client()


class TestListCustomers:

    def test_list_empty(self, client):
        response = client.get('/api/v1/customers')
        assert response.status_code == 200
        data = response.get_json()
        assert data['customers'] == []
        assert data['total'] == 0

    def test_list_with_pagination(self, client):
        for i in range(5):
            client.post('/api/v1/customers', json={
                'name': f'Customer {i}',
                'email': f'customer{i}@test.com'
            })

        response = client.get('/api/v1/customers?limit=2&offset=1')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['customers']) == 2
        assert data['total'] == 5


class TestCreateCustomer:

    def test_create_valid(self, client):
        response = client.post('/api/v1/customers', json={
            'name': 'Alice Smith',
            'email': 'alice@example.com'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == 'Alice Smith'
        assert 'id' in data

    def test_create_missing_email(self, client):
        response = client.post('/api/v1/customers', json={
            'name': 'Alice Smith'
        })
        assert response.status_code == 400

    def test_create_duplicate_email(self, client):
        client.post('/api/v1/customers', json={
            'name': 'Alice',
            'email': 'alice@example.com'
        })
        response = client.post('/api/v1/customers', json={
            'name': 'Bob',
            'email': 'alice@example.com'
        })
        assert response.status_code == 409


class TestGetCustomer:

    def test_get_existing(self, client):
        create_response = client.post('/api/v1/customers', json={
            'name': 'Bob',
            'email': 'bob@example.com'
        })
        customer_id = create_response.get_json()['id']

        response = client.get(f'/api/v1/customers/{customer_id}')
        assert response.status_code == 200
        assert response.get_json()['name'] == 'Bob'

    def test_get_not_found(self, client):
        response = client.get('/api/v1/customers/99999')
        assert response.status_code == 404
