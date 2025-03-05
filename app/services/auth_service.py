from ..models import User
from ..utils import ErrorResponse
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt

class AuthService:
    @staticmethod
    def register_user(email, password):
        if not email:
            raise ErrorResponse("Email is required", 400)
        if not password:
            raise ErrorResponse("Password is required", 400)
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            raise ErrorResponse("Email already registered", 409)
        new_user = User(
            email=email,
            password=generate_password_hash(password)
        )

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ErrorResponse(e, 500)
        return {'message': 'User created successfully'}
   
    @staticmethod
    def login(email, password):
        if not email or not password:
            raise ErrorResponse("Proper Credentials not provided", 400)

        user = User.query.filter_by(email = email).first()
        if not user:
            raise ErrorResponse("That account doesn't exist. Please create a new account.", 401)
        
        if check_password_hash(user.password, password):
            token = jwt.encode({
                'ulid': user.ulid,
                'exp': datetime.utcnow() + timedelta(minutes= 30)
            }, "secret", "HS256")
            return token
        #  password is wrong
        raise ErrorResponse("Credentials doesn't exist", 401)