import pytest
from app import create_app
from flask import jsonify
from unittest.mock import patch
from app.services import ServerService
from app.utils import ErrorResponse

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

#  create_server
@patch('app.services.ServerService.create_server')
def test_create_server_route(mock_create_server, client):
    mock_create_server.return_value = {'message': 'Server created successfully', 'server': {'server_name': 'New Server'}}
    
    response = client.post('/servers', json={'server_name': 'New Server'})
    
    assert response.status_code == 201
    assert response.json['message'] == 'Server created successfully'

#  health_check
@patch('app.services.ServerService.health_check')
def test_health_check_route(mock_health_check, client):
    mock_health_check.return_value = {'server_name': 'Server 1'}
    
    response = client.get('/health/some-ulid')
    
    assert response.status_code == 200
    assert response.json['server_name'] == 'Server 1'

# health_check_all
@patch('app.services.ServerService.health_check_all')
def test_health_check_all_route(mock_health_check_all, client):
    mock_health_check_all.return_value = [{'server_name': 'Server 1'}, {'server_name': 'Server 2'}]
    
    response = client.get('/health/all')
    
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]['server_name'] == 'Server 1'
    assert response.json[1]['server_name'] == 'Server 2'

# server registered
@patch('app.services.ServerService.create_server')
def test_create_server_name_exists_route(mock_create_server, client):
    mock_create_server.side_effect = ErrorResponse('Server name already registered', 409)
    
    response = client.post('/servers', json={'server_name': 'Existing Server'})
    
    assert response.status_code == 409
    assert response.json['message'] == 'Server name already registered'
