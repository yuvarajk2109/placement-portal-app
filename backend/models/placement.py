from extensions import db
from datetime import datetime

class Placement(db.Model):
    __tablename__ = 'placement'

    placement_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.application_id'), unique = True, nullable = False)
    position = db.Column(db.String(200), nullable = False)
    drive_type = db.Column(db.String(50), nullable = False)
    salary = db.Column(db.Float, nullable = True)
    joining_date = db.Column(db.Date, nullable = True)
    created_at = db.Column(db.DateTime, default = datetime.now, nullable = False)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now, nullable = False)