from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(255), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    role = db.Column(db.String(10), nullable = False) # we have 3 roles: Admin, Company, Student
    is_active = db.Column(db.Boolean, default = True, nullable = False)
    is_blacklisted = db.Column(db.Boolean, default = False, nullable = False)
    otp_code = db.Column(db.String(6), nullable = True)
    otp_expires_at = db.Column(db.DateTime, nullable = True)
    is_verified = db.Column(db.Boolean, default = False, nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.now(datetime.timezone.utc), nullable = False)
    updated_at = db.Column(db.DateTime, default = datetime.now(datetime.timezone.utc), onupdate = datetime.now(datetime.timezone.utc), nullable = False)

    student = db.relationship('Student', backref='user', uselist = False, lazy = True)
    company = db.relationship('Company', backref='user', uselist = False, lazy = True)

    def __repr__(self):
        return f'<User {self.email} ({self.role})'