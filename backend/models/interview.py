from extensions import db
from datetime import datetime

class Interview(db.Model):
    __tablename__ = 'interview'

    interview_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.drive_id'), nullable = False)
    round_number = db.Column(db.Integer, default = 1, nullable = False)
    round_title = db.Column(db.String(100), nullable = False)
    interview_date = db.Column(db.DateTime, nullable = False)
    location = db.Column(db.String(255), nullable = True)
    created_at = db.Column(db.DateTime, default = datetime.now(datetime.timezone.utc), nullable = False)

    __table_args__ = (
        db.UniqueConstraint('drive_id', 'round_number', name='unique_round_per_drive')
    )