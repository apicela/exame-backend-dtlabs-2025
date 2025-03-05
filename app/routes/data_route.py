from app.models import data
from flask import request, jsonify, Blueprint
from app.services import DataService
from app.utils import ErrorResponse
from app.utils import AuthUtils
from datetime import datetime

data_route = Blueprint('data_route', __name__)

@data_route.route('/data', methods=['POST'])
def insert_data():
    data = request.json
    server_ulid = data.get('server_ulid')
    timestamp = data.get('timestamp')
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    voltage = data.get('voltage')
    current = data.get('current')

    try:
        return jsonify(DataService.insert_data(server_ulid, timestamp, temperature, humidity, voltage, current)), 201
    except ErrorResponse as e:
        return jsonify(e.getMessage()), e.status_code
    except Exception as e:
        return jsonify({'message': 'Erro interno', 'error': str(e)}), 500
    
@data_route.route('/data', methods=['GET'])
@AuthUtils.token_required
def get_data(current_user):
    data = request.args
    server_ulid = data.get('server_ulid')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    sensor_type = data.get('sensor_type')
    aggregation = data.get('aggregation')

    try:
        return jsonify(DataService.get_data(current_user, server_ulid, start_time, end_time, sensor_type, aggregation)), 201
    except ErrorResponse as e:
        return jsonify(e.getMessage()), e.status_code
    except Exception as e:
        return jsonify({'message': 'Erro interno', 'error': str(e)}), 500
