import pytest
from unittest.mock import patch, MagicMock
from app.services import ServerService
from app.models import Server
from app.utils import ErrorResponse

#  create_server
@patch('app.services.db.session.add')
@patch('app.services.db.session.commit')
@patch('app.services.Server.query.filter_by')
def test_create_server(mock_filter, mock_commit, mock_add):
    #  mock
    mock_server = MagicMock(spec=Server)
    mock_filter.return_value.first.return_value = None  # Nenhum servidor existente
    mock_add.return_value = None
    mock_commit.return_value = None
    
    response = ServerService.create_server("New Server", "some-user-id")
    
    assert response['message'] == 'Server created successfully'
    assert response['server'] is not None

@patch('app.services.Server.query.filter_by')
def test_create_server_name_exists(mock_filter):
    mock_existing_server = MagicMock(spec=Server)
    mock_filter.return_value.first.return_value = mock_existing_server  # Servidor já existente
    
    with pytest.raises(ErrorResponse) as exc_info:
        ServerService.create_server("Existing Server", "some-user-id")
    
    assert exc_info.value.status_code == 409
    assert exc_info.value.getMessage() == 'Server name already registered'

@patch('app.services.Server.query.filter_by')
def test_health_check_all(mock_filter):
    mock_server1 = MagicMock(spec=Server)
    mock_server1.to_dict.return_value = {'server_name': 'Server 1'}
    
    mock_server2 = MagicMock(spec=Server)
    mock_server2.to_dict.return_value = {'server_name': 'Server 2'}
    
    mock_filter.return_value.all.return_value = [mock_server1, mock_server2]
    
    response = ServerService.health_check_all("some-user-id")
    
    assert len(response) == 2
    assert response[0]['server_name'] == 'Server 1'
    assert response[1]['server_name'] == 'Server 2'

#  método health_check
@patch('app.services.Server.query.filter_by')
def test_health_check_server_not_found(mock_filter):
    mock_filter.return_value.first.return_value = None
    
    with pytest.raises(ErrorResponse) as exc_info:
        ServerService.health_check("some-user-id", "some-ulid")
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.getMessage() == 'Server not found'
