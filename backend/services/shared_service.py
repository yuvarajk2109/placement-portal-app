from config import Config
from extensions import db
from models.skill import Skill
from models.branch import Branch
from models.student import Student
from models.user import User
from models.company import Company
from models.placement import Placement
from sqlalchemy import func

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
    
    @staticmethod
    def list_drive_types():
        return {
            "drive_types": Config.VALID_DRIVE_TYPES
        }, 200
    
    @staticmethod
    def list_application_statuses():
        return {
            "application_statuses": Config.STUDENT_APPLICATION_STATUSES
        }, 200
    
    @staticmethod
    def list_application_actions():
        return {
            "application_actions": Config.APPLICATION_ACTIONS
        }, 200
    
    @staticmethod
    def get_dashboard():
        total_students = Student.query.join(User).filter(User.is_blacklisted == False).count()
        total_companies = Company.query.join(User).filter(User.is_blacklisted == False).count()
        total_placements = Placement.query.count()
        avg_placement_salary = db.session.query(func.avg(Placement.salary)).scalar() or 0
        return {
            "total_students": total_students,
            "total_companies": total_companies,
            "total_placements": total_placements,
            "avg_placement_salary": avg_placement_salary
        }, 200