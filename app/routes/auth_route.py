from app.models import User
from flask import request, jsonify, Blueprint
from app.services import AuthService
from app.utils import ErrorResponse

auth_route = Blueprint('auth_route', __name__)

@auth_route.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    try:
        return jsonify(AuthService.register_user(email, password)), 201
    except ErrorResponse as e:
        return jsonify(e.getMessage()), e.status_code
    except Exception as e:
        return jsonify({'message': 'Erro interno', 'error': str(e)}), 500
