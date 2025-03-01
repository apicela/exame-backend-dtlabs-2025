from app.extensions import db
import ulid

class Data(db.Model):
    __tablename__ = 'Datas'
    id = db.Column(db.String(26), primary_key=True, default=lambda: str(ulid.new()), unique=True, nullable=False)
    server_ulid = db.Column(db.String(26), db.ForeignKey("Servers.server_ulid"), nullable=False) 
    timestamp = db.Column(db.DateTime, nullable=False)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    voltage = db.Column(db.Float,)
    current = db.Column(db.Float)