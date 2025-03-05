from app.models import server
from flask import request, jsonify, Blueprint
from app.services import ServerService
from app.utils import ErrorResponse
from app.utils import AuthUtils
server_route = Blueprint('ServerRoute', __name__)

@server_route.route('/servers', methods=['POST'])
@AuthUtils.token_required
def create_server(current_user):
    data = request.json
    server_name = data.get('server_name')
    try:
        return jsonify(ServerService.create_server(server_name, current_user)), 201
    except ErrorResponse as e:
        return jsonify(e.getMessage()), e.status_code
    except Exception as e:
        return jsonify({'message': 'Erro interno', 'error': str(e)}), 500
    
@server_route.route('/health/<ulid>', methods=['GET'])
@AuthUtils.token_required
def health_check(current_user, ulid):
    try:
        return jsonify(ServerService.health_check(current_user, ulid)), 200
    except ErrorResponse as e:
        return jsonify({'message:' : e.getMessage()}), e.status_code
    except Exception as e:
        return jsonify({'message': 'Erro interno', 'error': str(e)}), 500
    
@server_route.route('/health/all', methods=['GET'])
@AuthUtils.token_required
def health_check_all(current_user):
    try:
        return jsonify(ServerService.health_check_all(current_user)), 200
    except ErrorResponse as e:
        return jsonify({'message:' : e.getMessage()}), e.status_code
    except Exception as e:
        return jsonify({'message': 'Erro interno', 'error': str(e)}), 500