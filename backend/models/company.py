from extensions import db
from datetime import datetime

class Company(db.Model):
    __tablename__ = 'company'

    company_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), unique = True, nullable = False)
    company_name = db.Column(db.String(255), nullable = False)
    industry = db.Column(db.String(100), nullable = True)
    website = db.Column(db.String(255), nullable = True)
    location = db.Column(db.String(255), nullable = True)
    description = db.Column(db.Text, nullable = True)
    hr_name = db.Column(db.String(100), nullable = True)
    hr_email = db.Column(db.String(255), nullable = False)
    hr_phone = db.Column(db.String(15), nullable = True)
    status = db.Column(db.String(20), default = 'pending', nullable = False) # pending, approved, rejected'
    created_at = db.Column(db.DateTime, default = datetime.now, nullable = False)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now, nullable = False)

    drives = db.relationship('PlacementDrive', backref = 'company', lazy = True)

    def __repr__(self):
        return f'<Company {self.company_name} ({self.status})>'