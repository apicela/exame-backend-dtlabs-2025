from ..models import User
from ..utils import ErrorResponse
from app.extensions import db

class AuthService:
    @staticmethod
    def register_user( email, password):
        if not email:
            raise ErrorResponse("Email is required", 400)
        if not password:
            raise ErrorResponse("Password is required", 400)
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            raise ErrorResponse("Email already registered", 409)  
   
        new_user = User(
            email=email,
            password=password
        )

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ErrorResponse(e, 500)

        return new_user
