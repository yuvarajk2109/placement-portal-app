from extensions import db
from datetime import datetime

class Application(db.Model):
    __tablename__ = 'application'

    application_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    register_no = db.Column(db.String(20), db.ForeignKey('student.register_no'), nullable = False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.drive_id'), nullable = False)
    applied_date = db.Column(db.DateTime, default = datetime.now, nullable = False)
    application_status = db.Column(db.String(20), default = 'applied', nullable = False) # applied, shortlisted, rejected, selected
    current_round_id = db.Column(db.Integer, db.ForeignKey('interview.interview_id'), nullable = True)
    feedback = db.Column(db.Text, nullable = True)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now, nullable = False)

    current_round = db.relationship('Interview', backref = 'applications', lazy = True)
    placement = db.relationship('Placement', backref = 'application', uselist = False, lazy = True)

    __table_args__ = (
        db.UniqueConstraint('register_no', 'drive_id', name='unique_application_per_student_per_drive'),
    )