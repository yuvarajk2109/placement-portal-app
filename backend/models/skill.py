from extensions import db


class Skill(db.Model):
    __tablename__ = 'skill'

    skill_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    skill_name = db.Column(db.String(255), unique = True, nullable = False)