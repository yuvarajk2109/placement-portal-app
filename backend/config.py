import os
from dotenv import load_dotenv

def get_wsl_host_ip():
    try:
        import subprocess
        result = subprocess.run(['ip', 'route', 'show', 'default'], capture_output=True, text=True)
        if result.returncode == 0:
            parts = result.stdout.strip().split()
            if 'via' in parts:
                return parts[parts.index('via') + 1]
    except Exception:
        pass
        
    try:
        with open('/etc/resolv.conf', 'r') as f:
            for line in f:
                if line.startswith('nameserver'):
                    return line.split()[1].strip()
    except Exception:
        pass
    return '127.0.0.1'

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'yuvaraj_k')
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'uploads')

    DATABASE_PATH = os.path.abspath(os.path.join(ROOT_DIR, "db", "placement_portal.db"))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ITEMS_PER_PAGE = 5

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'yuvaraj_k_jwt_secret_key_long_secure_string_bruv')
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_REFRESH_TOKEN_EXPIRES = 86400

    default_mail_server = get_wsl_host_ip() if os.environ.get('WSL_DISTRO_NAME') else '127.0.0.1'
    MAIL_SERVER = os.getenv('MAIL_SERVER', default_mail_server)
    MAIL_PORT = int(os.getenv('MAIL_PORT', 1025))
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'Placement Portal <admin@placementportal.com>')

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
        'Selected for Next Round',
        'Selected',
        'Rejected',
        'Withdrawn',
        'Inactive',
        'Not Applied',
    ]

    APPLICATION_ACTIONS = [
        'Shortlisted', 
        'Selected for Next Round', 
        'Selected', 
        'Rejected'
    ]

    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/1')

    DEFAULT_TTL = 300
    
    DAILY_REMINDER_HOUR = 19
    DAILY_REMINDER_MINUTE = 0
    DAILY_REMINDER_DEADLINE = 3
    MONTHLY_REPORT_DAY = 15
    MONTHLY_REPORT_HOUR = 19
    MONTHLY_REPORT_MINUTE = 0
    EXPORT_FOLDER = os.path.join(UPLOAD_FOLDER, 'exports')