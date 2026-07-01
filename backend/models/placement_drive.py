from extensions import db
from datetime import datetime

drive_skill = db.Table('drive_skill',
    db.Column('drive_id', db.Integer, db.ForeignKey('placement_drive.drive_id'), primary_key = True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.skill_id'), primary_key = True)
)

drive_branch = db.Table('drive_branch',
    db.Column('drive_id', db.Integer, db.ForeignKey('placement_drive.drive_id'), primary_key = True),
    db.Column('branch_id', db.Integer, db.ForeignKey('branch.branch_id'), primary_key = True)
)

class PlacementDrive(db.Model):
    __tablename__ = 'placement_drive'

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

    drive_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'), nullable = False)
    job_title = db.Column(db.String(255), nullable = False)
    job_desc = db.Column(db.Text, nullable = False)
    drive_type = db.Column(db.String(100), nullable = False)
    cgpa_requirement = db.Column(db.Float, default = 0.0, nullable = False)
    salary_min = db.Column(db.Float, nullable = True)
    salary_max = db.Column(db.Float, nullable = False)
    location = db.Column(db.String(255), nullable = True)
    application_deadline = db.Column(db.DateTime, nullable = False)
    status = db.Column(db.String(20), default = 'Upcoming', nullable = False) # upcoming, ongoing, completed
    created_at = db.Column(db.DateTime, default = datetime.now, nullable = False)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now, nullable = False)

    eligible_branches = db.relationship('Branch', secondary=drive_branch, backref = 'placement_drives', lazy = True)
    interviews = db.relationship('Interview', backref = 'placement_drive', lazy = True)
    applications = db.relationship('Application', backref = 'placement_drive', lazy = True)
    required_skills = db.relationship('Skill', secondary=drive_skill, backref = db.backref('placement_drives', lazy = 'dynamic'))