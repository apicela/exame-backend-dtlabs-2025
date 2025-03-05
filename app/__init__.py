from flask import Flask
from app.extensions import db
from app.routes import auth_route, server_route, data_route
import os
import threading
from app.utils import RedisUtils

app = Flask(__name__)

# Configurações do Flask
app.config['FLASK_ENV'] = os.getenv('FLASK_ENV', 'production')  # Define o ambiente (development/production)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'uma_chave_secreta_muito_segura')

# Configuração do banco de dados (PostgreSQL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db with the app
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

app.register_blueprint(auth_route)
app.register_blueprint(server_route)
app.register_blueprint(data_route)

redisUtils = RedisUtils(app)
processing_thread = threading.Thread(target=redisUtils.process_data, daemon=True)
processing_thread.start()

if __name__ == '__main__':
    app.run(debug=True)