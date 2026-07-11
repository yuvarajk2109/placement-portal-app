from config import Config
from extensions import db
from models.user import User
from models.student import Student
from models.skill import Skill
from models.company import Company
from models.placement_drive import PlacementDrive
from models.application import Application
from models.placement import Placement

import os
from flask import send_file
from werkzeug.utils import secure_filename
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class StudentService:

    @staticmethod
    def get_dashboard(user_id):
        student = Student.query.filter_by(user_id = user_id).first()
        if not student:
            return {
                "error": "Student not found"
            }, 404
        
        drive_query = PlacementDrive.query.filter(PlacementDrive.status == 'Approved', PlacementDrive.application_deadline > datetime.now())
        if student.year_of_study == 3:
            drive_query = drive_query.filter(PlacementDrive.drive_type == '2M Internship')
        elif student.year_of_study == 4:
            drive_query = drive_query.filter(PlacementDrive.drive_type != '2M Internship')

        eligible_drives_count = drive_query.count()

        applications = Application.query.filter_by(register_no = student.register_no).all()
        total_applications = len(applications)
        status_counts = {}
        for application in applications:
            status_counts[application.application_status] = status_counts.get(application.application_status, 0) + 1
        
        is_placed = any(
            Placement.query.filter_by(application_id = application.application_id).first() is not None
            for application in applications
        )

        return {
            "register_no": student.register_no,
            "student_name": f"{student.fname} {student.lname}",
            "year_of_study": student.year_of_study,
            "cgpa": student.cgpa,
            "eligible_drives_count": eligible_drives_count,
            "total_applications": total_applications,
            "application_status_counts": status_counts,
            "is_placed": is_placed
        }, 200

    @staticmethod
    def get_profile(user_id):
        student = Student.query.filter_by(user_id = user_id).first()
        if not student:
            return {
                "error": "Student not found"
            }, 404
        
        user = User.query.get(user_id)

        resume = os.path.basename(student.resume_path) if student.resume_path else None

        return {
            "register_no": student.register_no,
            "email": user.email if user else None,
            "fname": student.fname,
            "lname": student.lname,
            "dob": student.dob.isoformat() if student.dob else None,
            "phone": student.phone,
            "cgpa": student.cgpa,
            "year_of_study": student.year_of_study,
            "branch_name": student.branch.branch_name if student.branch else None,
            "resume": resume,
            "skill_ids": [skill.skill_id for skill in student.skills],
            "created_at": student.created_at.isoformat()
        }, 200
    
    @staticmethod
    def update_profile(user_id, data):
        student = Student.query.filter_by(user_id = user_id).first()
        if not student:
            return {
                "error": "Student not found"
            }, 404
        
        updatable = ['fname', 'lname', 'dob', 'phone', 'cgpa']
        for field in updatable:
            if field in data:
                if field == 'dob' and isinstance(data[field], str):
                    try:
                        setattr(student, field, datetime.strptime(data[field], '%Y-%m-%d').date())
                    except ValueError:
                        return {
                            "error": "Invalid dob format. Use YYYY-MM-DD"
                        }, 400
                else:
                    setattr(student, field, data[field])
        
        if 'skill_ids' in data:
            student.skills.clear()
            if data['skill_ids']:
                updated_skills = Skill.query.filter(Skill.skill_id.in_(data['skill_ids'])).all()
                student.skills.extend(updated_skills)

        db.session.commit()
        logger.info(f"Student {student.fname} {student.lname}'s ({student.register_no}) profile updated")
        return {
            "message": "Student profile updated successfully"
        }, 200
    
    @staticmethod
    def upload_resume(user_id, file):
        student = Student.query.filter_by(user_id = user_id).first()
        if not student:
            return {
                "error": "Student not found"
            }, 404
        
        filename = secure_filename(file.filename)
        extension = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        if extension not in Config.ALLOWED_RESUME_EXTENSIONS:
            return {
                "error": f"Invalid file type. Allowed extensions: {Config.ALLOWED_RESUME_EXTENSIONS}"
            }, 400
        
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        if size > Config.MAX_RESUME_SIZE:
            return {
                "error": f"File too large. Maximum allowed size is {Config.MAX_RESUME_SIZE}."
            }, 413
    
        os.makedirs(Config.RESUME_FOLDER, exist_ok = True)

        if student.resume_path and os.path.exists(student.resume_path):
            os.remove(student.resume_path)

        file_name = f"{student.register_no}_resume.{extension}"
        file_path = os.path.join(Config.RESUME_FOLDER, file_name)
        file.save(file_path)

        student.resume_path = file_path
        db.session.commit()

        logger.info(f"Student {student.fname} {student.lname} ({student.register_no} uploaded resume: {file_name})")
        return {
            "message": "Resume uploaded successfully",
            "filename": file_name
        }, 200
    
    @staticmethod
    def download_resume(user_id):
        student = Student.query.filter_by(user_id = user_id).first()
        if not student or not student.resume_path:
            return {
                "error": "Resume not found"
            }, 404
        
        if not os.path.exists(student.resume_path):
            return {
                "error": "Resume file missing from server"
            }, 404
        
        return send_file(
            student.resume_path,
            as_attachment = True,
            download_name = os.path.basename(student.resume_path)
        )
    
    @staticmethod
    def list_eligible_drives(user_id, search, location, drive_type, min_salary, page, per_page):
        student = Student.query.filter_by(user_id = user_id).first()
        if not student:
            return {
                "error": "Student not found"
            }, 404
        
        query = PlacementDrive.query.filter(PlacementDrive.status == 'Approved', PlacementDrive.application_deadline > datetime.now())

        if student.year_of_study == 3:
            query = query.filter(PlacementDrive.drive_type == '2M Internship')
        elif student.year_of_study == 4:
            query = query.filter(PlacementDrive.drive_type != '2M Internship')
        
        if search:
            query = query.filter(PlacementDrive.job_title.ilike(f"%{search}%"))
        if location:
            query = query.filter(PlacementDrive.location.ilike(f"%{location}%"))
        if drive_type:
            query = query.filter(PlacementDrive.drive_type == drive_type)
        if min_salary is not None:
            query = query.filter(PlacementDrive.salary_max >= min_salary)

        pagination = query.order_by(PlacementDrive.application_deadline.asc()).paginate(
            page = page,
            per_page = per_page,
            error_out = False
        )

        drives = []
        for drive in pagination.items:
            drives.append({
                "drive_id": drive.drive_id,
                "job_title": drive.job_title,
                "company_name": drive.company.company_name if drive.company else None,
                "drive_type": drive.drive_type,
                "cgpa_requirement": drive.cgpa_requirement,
                "salary_min": drive.salary_min,
                "salary_max": drive.salary_max,
                "location": drive.location,
                "application_deadline": drive.application_deadline.isoformat() if drive.application_deadline else None,
                "required_skills": [
                    {
                        "skill_id": skill.skill_id,
                        "skill_name": skill.skill_name
                    }
                    for skill in drive.required_skills
                ]
            })

        return {
            "drives": drives,
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages
        }, 200
    
    @staticmethod
    def get_drive_details(user_id, drive_id):
        student = Student.query.filter_by(user_id = user_id).first()
        if not student:
            return {
                "error": "Student not found"
            }, 404
        
        drive = PlacementDrive.query.get(drive_id)
        if not drive or drive.status != 'Approved':
            return {
                "error": "Drive not found"
            }, 404
        
        company = Company.query.get(drive.company_id)
        existing_application = Application.query.filter_by(register_no = student.register_no, drive_id = drive_id).first()

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
            "company_name": company.company_name if company else None,
            "company_industry": company.industry if company else None,
            "eligible_branches": [
                {
                "branch_id": branch.branch_id,
                "branch_name": branch.branch_name
                }
                for branch in drive.eligible_branches
            ],
            "required_skills": [
                {
                    "skill_id": skill.skill_id,
                    "skill_name": skill.skill_name
                }
                for skill in drive.required_skills
            ],
            "interviews": [
                {
                    "round_number": interview.round_number,
                    "round_title": interview.round_title,
                    "interview_date": interview.interview_date.isoformat() if interview.interview_date else None,
                    "location": interview.location,
                }
                for interview in drive.interviews
            ],
            "already_applied": existing_application is not None,
            "application_status": existing_application.application_status if existing_application else None
        }, 200
    
    @staticmethod
    def get_placement(user_id):
        student = Student.query.filter_by(user_id = user_id).first()
        if not student:
            return {
                "error": "Student not found"
            }, 404
        
        placement = Placement.query.join(Application).filter(Application.register_no == student.register_no ).first()
        if not placement:
            return {
                "error": "No placement found for this student."
            }, 404
        
        drive = PlacementDrive.query.join(Application).filter(Application.application_id == placement.application_id).first()
        company = Company.query.get(drive.company_id) if drive else None

        placement_record = {
            "placement_id": placement.placement_id,
            "position": placement.position,
            "drive_type": placement.drive_type,
            "salary": placement.salary,
            "joining_date": placement.joining_date.isoformat() if placement.joining_date else None,
            "job_title": drive.job_title if drive else None,
            "company_name": company.company_name if company else None,
            "created_at": placement.created_at.isoformat()
        }

        return {
            "placement": placement_record
        }, 200