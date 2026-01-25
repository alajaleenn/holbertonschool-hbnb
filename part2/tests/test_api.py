"""Unit tests for HBnB API endpoints."""
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

@pytest.fixture
def client():
    app = create_app('development')
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_user(client):
    response = client.post('/api/v1/users/', json={'first_name': 'Test', 'last_name': 'User', 'email': 'test@example.com'})
    assert response.status_code == 201
    
def test_get_users(client):
    response = client.get('/api/v1/users/')
    assert response.status_code == 200
