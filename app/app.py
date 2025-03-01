# app/__init__.py
from flask import Flask
from app.extensions import db
from app.routes import auth_route
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

# Initialize db with the app
db.init_app(app)


# Create tables
with app.app_context():
    db.create_all()
app.register_blueprint(auth_route)

if __name__ == '__main__':
    app.run(debug=True)