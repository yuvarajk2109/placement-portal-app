from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
import redis
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()
cors = CORS()

try:
    redis_client = redis.from_url(Config.REDIS_URL)
    redis_client.ping()
except Exception:
    redis_client = None