import pytest
from flask import Flask
from app import create_app
from app.models import Data
from app.extensions import db
from unittest.mock import patch
from datetime import datetime

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_insert_data_route(client):
    # Simulate a valid POST request
    with patch('app.services.DataService.insert_data') as mock_insert_data:
        mock_insert_data.return_value = {'message': 'Data inserted successfully'}
        response = client.post('/data', json={
            'server_ulid': 'test-ulid',
            'timestamp': '2025-03-05 12:00:00.000',
            'temperature': 25.5,
            'humidity': 60,
            'voltage': 220,
            'current': 5
        })
        assert response.status_code == 201
        assert response.json == {'message': 'Data inserted successfully'}

def test_insert_data_route_missing_timestamp(client):
    response = client.post('/data', json={
        'server_ulid': 'test-ulid',
        'timestamp': '',
        'temperature': 25.5,
        'humidity': 60,
        'voltage': 220,
        'current': 5
    })
    assert response.status_code == 400
    assert 'Timestamp is required' in response.json['message']

def test_get_data_route(client):
    # Simulate a valid GET request
    with patch('app.services.DataService.get_data') as mock_get_data:
        mock_get_data.return_value = [{'timestamp': '2025-03-05 12:00:00.000', 'temperature': 25.5}]
        response = client.get('/data', query_string={
            'server_ulid': 'test-ulid',
            'start_time': '2025-03-05 12:00:00.000',
            'end_time': '2025-03-05 12:30:00.000',
            'sensor_type': 'temperature',
            'aggregation': 'minute'
        })
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) > 0
