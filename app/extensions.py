# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
import redis
import os

db = SQLAlchemy()
redis_url = os.getenv('REDIS_URL', 'redis://redis_cache:6379/0')  # Alterado para o nome do serviço no Docker Compose
redis_client = redis.Redis.from_url(redis_url)
