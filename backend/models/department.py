from extensions import db

class Department(db.Model):
    __tablename__ = 'department'

    dept_id = db.Column(db.Integer, primary_key = True)
    dept_name = db.Column(db.String(100), unique = True, nullable = False)

    branches = db.relationship('Branch', backref = 'department', lazy = True)