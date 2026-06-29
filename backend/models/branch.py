from extensions import db

class Branch(db.Model):
    __tablename__ = 'branch'

    branch_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    branch_name = db.Column(db.String(100), unique = True, nullable = False)
    dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'), nullable = False)

    __table_args__ = (
        db.UniqueConstraint('branch_name', 'dept_id', name='unique_branch_per_department'),
    )