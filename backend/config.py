import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'yuvaraj_k')
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'uploads')

    DATABASE_PATH = os.path.abspath(os.path.join(ROOT_DIR, "db", "placement_portal.db"))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'yuvaraj_k_jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_REFRESH_TOKEN_EXPIRES = 86400

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'Starspinix')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'pbqd dxrv olub rqcr')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'starspinix@gmail.com')

    RESUME_FOLDER = os.path.join(UPLOAD_FOLDER, 'resumes')
    ALLOWED_RESUME_EXTENSIONS = {'pdf', 'doc', 'docx'}
    MAX_RESUME_SIZE = 5 * 1024 * 1024

    VALID_DRIVE_TYPES = [
        '2M Internship',
        '5M Internship',
        '6M Internship',
        '5M Internship + Placement',
        '6M Internship + Placement',
        '5M Internship + Performance-based Placement',
        '6M Internship + Performance-based Placement',
        'Direct Placement'
    ]

    STUDENT_APPLICATION_STATUSES = [
        'Applied',
        'Shortlisted',
        'Selected for Next Round'
        'Selected',
        'Rejected',
        'Withdrawn',
        'Not Applied'
    ]

    APPLICATION_ACTIONS = [
        'Shortlisted', 
        'Selected for Next Round', 
        'Selected', 
        'Rejected'
    ]