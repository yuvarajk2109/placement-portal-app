from extensions import db
from models.branch import Branch
from models.skill import Skill
from models.company import Company
from models.placement_drive import PlacementDrive
from models.application import Application
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DriveService:

    @staticmethod
    def create_drive(user_id, data):
        company = Company.query.filter_by(user_id = user_id).first()
        if not company:
            return {
                "error": "Company not found"
            }, 404
        if company.status != 'Approved':
            return {
                "error": "Only approved companies can create placement drives"
            }, 403
        
        if data['drive_type'] not in PlacementDrive.VALID_DRIVE_TYPES:
            return {
                "error": f"Invalid drive type. Valid types are: {PlacementDrive.VALID_DRIVE_TYPES}"
            }, 400
        
        try:
            deadline = datetime.fromisoformat(data['application_deadline'])
        except ValueError:
            return {
                "error": "Invalid date format for application_deadline. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
            }, 400
        
        drive = PlacementDrive(
            company_id = company.company_id,
            job_title = data['job_title'],
            job_desc = data['job_desc'],
            drive_type = data['drive_type'],
            cgpa_requirement = data['cgpa_requirement'],
            salary_min = data.get('salary_min'),
            salary_max = data['salary_max'],
            location = data.get('location'),
            application_deadline = deadline,
            status = 'Upcoming'
        )
        db.session.add(drive)
        db.session.flush()

        branch_ids = data.get('eligible_branches', [])
        if branch_ids:
            branches = Branch.query.filter(Branch.branch_id.in_(branch_ids)).all()
            drive.eligible_branches.extend(branches)

        skill_ids = data.get('skill_ids', [])
        if skill_ids:
            skills = Skill.query.filter(Skill.skill_id.in_(skill_ids)).all()
            drive.required_skills.extend(skills)

        db.session.commit()

        logger.info(f"Company {company.company_name} created drive '{drive.job_title}' of type {drive.drive_type}, with ID {drive.drive_id}")

        return {
            "message": "Placement drive created. Awaiting admin approval.",
            "drive_id": drive.drive_id,
            "drive_type": drive.drive_type,
        }, 201
    
    @staticmethod
    def list_company_drives(user_id, page, per_page):
        company = Company.query.filter_by(user_id = user_id).first()
        if not company:
            return {
                "error": "Company not found"
            }, 404
        
        pagination = PlacementDrive.query.filter_by(company_id = company.company_id).order_by(PlacementDrive.created_at.desc()).paginate(
            page = page,
            per_page = per_page,
            error_out = False
        )

        drives = []
        for drive in pagination.items:
            applications_count = len(drive.applications)
            drives.append({
                "drive_id": drive.drive_id,
                "job_title": drive.job_title,
                "drive_type": drive.drive_type,
                "status": drive.status,
                "application_deadline": drive.application_deadline.isoformat() if drive.application_deadline else None,
                "cgpa_requirement": drive.cgpa_requirement,
                "location": drive.location,
                "applications_count": applications_count,
                "created_at": drive.created_at.isoformat()
            })

        return {
            "drives": drives,
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages
        }
    
    @staticmethod
    def get_drive(user_id, drive_id, role = 'company'):
        drive = PlacementDrive.query.get(drive_id)
        if not drive:
            return {
                "error": "Drive not found"
            }, 404
        
        if role == 'company':
            company = Company.query.filter_by(user_id = user_id).first()
            if not company or drive.company_id != company.company_id:
                return {
                    "error": "Access denied"
                }, 403
            
        company = Company.query.get(drive.company_id)
        branches = [branch.branch_name for branch in drive.eligible_branches]
        required_skills = [skill.skill_name for skill in drive.required_skills]
        applications_count = len(drive.applications)

        return {
            "drive_id": drive.drive_id,
            "job_title": drive.job_title,
            "job_desc": drive.job_desc,
            "drive_type": drive.drive_type,
            "cgpa_requirement": drive.cgpa_requirement,
            "salary_min": drive.salary_min,
            "salary_max": drive.salary_max,
            "location": drive.location,
            "application_deadline": drive.application_deadline.isoformat() if drive.application_deadline else None,
            "status": drive.status,
            "company_name": company.company_name if company else None,
            "eligible_branches": branches,
            "required_skills": required_skills,
            "applications_count": applications_count,
            "interviews": [
                {
                    "interview_id": interview.interview_id,
                    "round_number": interview.round_number,
                    "round_title": interview.round_title,
                    "interview_date": interview.interview_date.isoformat() if interview.interview_date else None,
                    "location": interview.location,
                }
                for interview in drive.interviews
            ]
        }, 200
    
    @staticmethod
    def update_drive(user_id, drive_id, data):
        company = Company.query.filter_by(user_id = user_id).first()
        drive = PlacementDrive.query.get(drive_id)

        if not company or not drive or drive.company_id != company.company_id:
            return {
                "error": "Access denied"
            }, 403
        
        if drive.status not in {'Pending', 'Approved'}:
            return {
                "error": "Cannot update a closed or rejected drive"
            }, 400
        
        updatable = [
            'job_title',
            'job_desc',
            'cgpa_requirement',
            'salary_min',
            'salary_max',
            'location'
        ]
        for field in updatable:
            if field in data:
                setattr(drive, field, data[field])

        if 'application_deadline' in data:
            try:
                drive.application_deadline = datetime.fromisoformat(data['application_deadline'])
            except ValueError:
                return {
                    "error": "Invalid date format for application_deadline. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
                }, 400
            
        if 'drive_type' in data:
            if data['drive_type'] not in PlacementDrive.VALID_DRIVE_TYPES:
                return {
                    "error": f"Invalid drive type. Valid types are: {PlacementDrive.VALID_DRIVE_TYPES}"
                }, 400
            drive.drive_type = data['drive_type']

        if 'eligible_branch_ids' in data:
            branch_ids = data['eligible_branch_ids']
            branches = Branch.query.filter(Branch.branch_id.in_(branch_ids)).all()
            drive.eligible_branches = branches

        if 'skill_ids' in data:
            drive.required_skills.clear()
            new_skills = Skill.query.filter(Skill.skill_id.in_(data['skill_ids'])).all()
            drive.required_skills.extend(new_skills)

        db.session.commit()

        logger.info(f"Company {company.company_name} updated drive '{drive.job_title}' (ID: {drive.drive_id})")
        return {
            "message": "Drive updated successfully"
        }, 200
    
    @staticmethod
    def close_drive(user_id, drive_id):
        company = Company.query.filter_by(user_id = user_id).first()
        drive = PlacementDrive.query.get(drive_id)

        if not company or not drive or drive.company_id != company.company_id:
            return {
                "error": "Access denied"
            }, 403
        
        drive.status = 'Closed'
        db.session.commit()

        logger.info(f"Company {company.company_name} closed drive '{drive.job_title}' (ID: {drive.drive_id})")
        return {
            "message": "Drive closed successfully"
        }, 200
        