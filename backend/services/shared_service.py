from extensions import db
from models.skill import Skill
from models.branch import Branch

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

    @staticmethod
    def list_branches():
        branches = Branch.query.order_by(Branch.branch_name).all()
        return {
            "branches": [
                {
                    "branch_id": branch.branch_id,
                    "branch_name": branch.branch_name,
                    "dept_id": branch.dept_id
                }
                for branch in branches
            ]
        }, 200