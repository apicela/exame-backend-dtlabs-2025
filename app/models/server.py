from app.extensions import db
import ulid

class Server(db.Model):
    __tablename__ = 'Servers'
    server_ulid = db.Column(db.String(26), primary_key=True, default=lambda: str(ulid.new()), unique=True, nullable=False)
    server_name = db.Column(db.String(120), nullable=False, unique=True)
    datas = db.relationship('Data', backref='server', lazy=True)
    created_by = db.Column(db.String(26), db.ForeignKey("Users.ulid"), nullable=False)
    last_ping = db.Column(db.DateTime, nullable=True)

