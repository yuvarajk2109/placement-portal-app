from extensions import db
from models.skill import Skill

class SharedService:

    @staticmethod
    def list_skills():
        skills = Skill.query.order_by(Skill.skill_name).all()
        return {
            "skills": [
                {
                    "skill_id": skill.skill_id,
                    "skill_name": skill.skill_name
                }
                for skill in skills
            ]
        }, 200