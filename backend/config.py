import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'yuvaraj_k')
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    DATABASE_PATH = os.path.abspath(os.path.join(ROOT_DIR, "db", "placement_portal.db"))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'yuvaraj_k_jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_REFRESH_TOKEN_EXPIRES = 86400

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmal.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@placement.edu')