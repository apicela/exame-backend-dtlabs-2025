from app.extensions import db
import ulid
import datetime

class Server(db.Model):
    __tablename__ = 'Servers'
    server_ulid = db.Column(db.String(26), primary_key=True, default=lambda: str(ulid.new()), unique=True, nullable=False)
    server_name = db.Column(db.String(120), nullable=False, unique=True)
    datas = db.relationship('Data', backref='server', lazy=True)
    ownerUlid = db.Column(db.String(26), db.ForeignKey("Users.ulid"), nullable=False)
    last_ping = db.Column(db.DateTime, nullable=True)
    last_data_timestamp = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'server_ulid': self.server_ulid,
            'server_name': self.server_name,
            'last_ping': self.last_ping.isoformat() if self.last_ping else None,
            'last_data_timestamp': self.last_data_timestamp.isoformat() if self.last_data_timestamp else None,
            'ownerUlid': self.ownerUlid
        }