from functools import wraps
from flask import request, jsonify
import jwt
from app.models import User  # Importe seu modelo de usuário

class AuthUtils:
    @staticmethod
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization']
            
            if not token:
                return jsonify({"message": "Token is missing"}), 401
            
            try:
                data = jwt.decode(token, "secret", algorithms=["HS256"])
                current_user = User.query.filter_by(ulid=data["ulid"]).first().ulid
            except Exception as e:
                print(e)
                return jsonify({"message": "Token is invalid"}), 401

            return f(current_user, *args, **kwargs)
        return decorated
