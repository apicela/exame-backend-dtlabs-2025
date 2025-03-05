from ..models import Server
from ..utils import ErrorResponse, AuthUtils
from app.extensions import db

class ServerService:
    @staticmethod
    def create_server(server_name, userId):
        if not server_name:
            raise ErrorResponse("Server name is required", 400)
        existing_server = Server.query.filter_by(server_name=server_name).first()
        if existing_server:
            raise ErrorResponse("Server name already registered", 409)
        new_server = Server(
            server_name=server_name,
            ownerUlid=userId
        )
        try:
            db.session.add(new_server)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            raise ErrorResponse(e, 500)
        return {'message': 'Server created successfully', 'server': new_server.to_dict()}
    
    @staticmethod
    def health_check_all(current_user):
        servers = Server.query.filter_by(ownerUlid=current_user).all()
        return [server.to_dict() for server in servers]
    
    def health_check(current_user, ulid):
        server = Server.query.filter_by(ownerUlid=current_user, ulid=ulid).first()
        if not server:
            raise ErrorResponse("Server not found", 404)
        return server.to_dict()
    
    def get_server(ulid):
        server = Server.query.filter_by(server_ulid=ulid).first()
        if not server:
            raise ErrorResponse("Server not found", 404)
        return server