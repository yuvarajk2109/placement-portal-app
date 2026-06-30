from extensions import db
from datetime import datetime

student_skill = db.Table('student_skill',
    db.Column('register_no', db.String(10), db.ForeignKey('student.register_no'), primary_key = True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.skill_id'), primary_key = True)
)

class Student(db.Model):
    __tablename__ = 'student'

    register_no = db.Column(db.String(10), primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), unique = True, nullable = False)
    fname = db.Column(db.String(100), nullable = False)
    lname = db.Column(db.String(100), nullable = False)
    dob = db.Column(db.Date, nullable = False)
    phone = db.Column(db.String(15), nullable = True)
    cgpa = db.Column(db.Float, default = 0.0, nullable = False)
    year_of_study = db.Column(db.Integer, nullable = False) # only 3 or 4 are allowed to register
    resume_path = db.Column(db.String(255), nullable = True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.branch_id'), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.now, nullable = False)
    updated_at = db.Column(db.DateTime, default = datetime.now, onupdate = datetime.now, nullable = False)

    branch = db.relationship('Branch', backref = 'students', lazy = True)
    applications = db.relationship('Application', backref = 'student', lazy = True)
    skills = db.relationship('Skill', secondary=student_skill, backref = db.backref('students', lazy = 'dynamic'))

    def __repr__(self):
        return f'<Student {self.register_no} - ({self.fname} {self.lname})>'