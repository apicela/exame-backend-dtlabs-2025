import pytest
from datetime import datetime, timedelta
from app.services import DataService
from app.utils import ErrorResponse
from app.models import Data
from unittest.mock import patch
from app.extensions import db

@pytest.fixture
def mock_server():
    # Mock server for testing
    server = {
        'server_ulid': 'test-ulid',
        'last_data_timestamp': datetime.now() - timedelta(seconds=2),
        'last_ping': datetime.now()
    }
    return server

def test_insert_data_valid(mock_server):
    with patch('app.services.ServerService.get_server') as mock_get_server:
        mock_get_server.return_value = mock_server
        response = DataService.insert_data(
            'test-ulid', '2025-03-05 12:00:00.000', 25.5, 60, 220, 5
        )
        assert response == {'message': 'Data inserted successfully'}

def test_insert_data_missing_timestamp(mock_server):
    with patch('app.services.ServerService.get_server') as mock_get_server:
        mock_get_server.return_value = mock_server
        with pytest.raises(ErrorResponse):
            DataService.insert_data(
                'test-ulid', '', 25.5, 60, 220, 5
            )

def test_insert_data_invalid_timestamp(mock_server):
    with patch('app.services.ServerService.get_server') as mock_get_server:
        mock_get_server.return_value = mock_server
        with pytest.raises(ErrorResponse):
            DataService.insert_data(
                'test-ulid', 'invalid-timestamp', 25.5, 60, 220, 5
            )

def test_insert_data_missing_temperature_and_humidity(mock_server):
    with patch('app.services.ServerService.get_server') as mock_get_server:
        mock_get_server.return_value = mock_server
        with pytest.raises(ErrorResponse):
            DataService.insert_data(
                'test-ulid', '2025-03-05 12:00:00.000', None, None, 220, 5
            )

def test_insert_data_invalid_humidity(mock_server):
    with patch('app.services.ServerService.get_server') as mock_get_server:
        mock_get_server.return_value = mock_server
        with pytest.raises(ErrorResponse):
            DataService.insert_data(
                'test-ulid', '2025-03-05 12:00:00.000', 25.5, -10, 220, 5
            )

def test_insert_data_frequency_check(mock_server):
    # Simulate last_data_timestamp close to now (should raise error)
    mock_server['last_data_timestamp'] = datetime.now() - timedelta(seconds=0.05)
    with patch('app.services.ServerService.get_server') as mock_get_server:
        mock_get_server.return_value = mock_server
        with pytest.raises(ErrorResponse):
            DataService.insert_data(
                'test-ulid', '2025-03-05 12:00:00.000', 25.5, 60, 220, 5
            )

def test_get_data_valid(mock_server):
    # Simulate valid data fetch
    with patch('app.services.DataService.get_data') as mock_get_data:
        mock_get_data.return_value = [{'timestamp': '2025-03-05 12:00:00.000', 'temperature': 25.5}]
        response = DataService.get_data(
            'test-user', 'test-ulid', '2025-03-05 12:00:00.000', '2025-03-05 12:30:00.000', 'temperature', None
        )
        assert isinstance(response, list)
        assert len(response) > 0
