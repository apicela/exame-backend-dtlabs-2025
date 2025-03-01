from app.extensions import db
import ulid

class User(db.Model):
    __tablename__ = 'Users'
    ulid = db.Column(db.String(26), primary_key=True, default=lambda: str(ulid.new()), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    servers = db.relationship('Server', backref='user', lazy=True)