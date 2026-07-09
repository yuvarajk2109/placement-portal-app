from extensions import db
from models.user import User
from models.student import Student
from models.skill import Skill
from models.branch import Branch
from models.company import Company
from models.placement_drive import PlacementDrive
from models.application import Application 
from models.placement import Placement
import logging

logger = logging.getLogger(__name__)

class AdminService:

    @staticmethod
    def get_dashboard():
        total_students = Student.query.count()
        total_companies = Company.query.count()
        pending_companies = Company.query.filter_by(status = 'Pending').count()
        total_drives = PlacementDrive.query.count()
        pending_drives = PlacementDrive.query.filter_by(status = 'Pending').count()
        total_applications = Application.query.count()
        total_placements = Placement.query.count()

        return {
            "total_students": total_students,
            "total_companies": total_companies,
            "pending_companies": pending_companies,
            "total_drives": total_drives,
            "pending_drives": pending_drives,
            "total_applications":  total_applications,
            "total_placements": total_placements
        }, 200
    
    @staticmethod
    def list_companies(status_filter, search, page, per_page):
        query = Company.query.join(User).filter(
            db.or_(User.is_active == True, User.is_blacklisted == True)
        )

        if status_filter:
            query = query.filter(Company.status == status_filter)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                db.or_(
                    Company.company_name.ilike(search_term),
                    Company.industry.ilike(search_term),
                )
            )
        
        pagination = query.order_by(Company.created_at.desc()).paginate(
            page = page,
            per_page = per_page,
            error_out = False
        )

        companies = []
        for company in pagination.items:
            user = User.query.get(company.user_id)
            companies.append({
                "company_id": company.company_id,
                "company_name": company.company_name,
                "industry": company.industry,
                "location": company.location,
                "hr_email": company.hr_email,
                "status": company.status,
                "is_blacklisted": user.is_blacklisted if user else False,
                "created_at": company.created_at.isoformat()
            })

        return {
            "companies": companies,
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages
        }, 200
    
    @staticmethod
    def update_company_status(company_id, new_status):
        company = Company.query.get(company_id)
        if not company:
            return {
                "error": "Company not found"
            }, 404
        
        company.status = new_status
        db.session.commit()

        logger.info(f"Status of Company '{company.company_name}' updated to {new_status}.")
        return {
            "message": f"Company {new_status} successfully."
        }, 200
    
    @staticmethod
    def remove_company(company_id):
        company = Company.query.get(company_id)
        if not company:
            return {
                "error": "Company not found"
            }, 404
    
        user = User.query.get(company.user_id)
        
        if user:
            user.is_active = False
        company.status = 'Rejected'
        db.session.commit()

        logger.info(f"Company '{company.company_name}' removed (soft-delete)")
        return {
            "message": "Company removed successfully"
        }, 200
    
    @staticmethod
    def toggle_blacklist_company(company_id, blacklist):
        company = Company.query.get(company_id)
        if not company:
            return {
                "error": "Company not found"
            }, 404
        
        user = User.query.get(company.user_id)
        if not user:
            return {
                "error": "Associated user not found"
            }, 404
        
        user.is_blacklisted = blacklist
        if blacklist:
            user.is_active = False
        else:
            user.is_active = True
        db.session.commit()

        action = "blacklisted" if blacklist else "unblacklisted"
        logger.info(f"Company '{company.company_name}' {action}")
        return {
            "message": f"Company {action} successfully"
        }, 200
    
    @staticmethod
    def list_drives(status_filter, page, per_page):
        query = PlacementDrive.query
        
        if status_filter:
            query = query.filter(PlacementDrive.status == status_filter)

        pagination = query.order_by(PlacementDrive.created_at.desc()).paginate(
            page = page,
            per_page = per_page,
            error_out = False
        )

        drives = []
        for drive in pagination.items:
            company = Company.query.get(drive.company_id)
            drives.append({
                "drive_id": drive.drive_id,
                "job_title": drive.job_title,
                "company_name": company.company_name if company else None,
                "drive_type": drive.drive_type,
                "status": drive.status,
                "deadline": drive.application_deadline.isoformat() if drive.deadline else None,
                "applications_count": Application.query.filter_by(drive_id = drive.drive_id).count(),
                "created_at": drive.created_at.isoformat()
            })

        return {
            "drives": drives,
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages
        }, 200
    
    @staticmethod
    def update_drive_status(drive_id, new_status):
        drive = PlacementDrive.query.get(drive_id)
        if not drive:
            return {
                "error": "Drive not found"
            }, 404
        
        drive.status = new_status
        db.session.commit()

        logger.info(f"Status of Drive '{drive.job_title} (id = {drive_id}) updated to {new_status}")
        return {
            "message": f"Drive {new_status} successfully"
        }, 200
    
    @staticmethod
    def list_students(status_filter, search, page, per_page):
        query = Student.query.join(User)
        
        if status_filter == 'Active':
            query = query.filter(User.is_active == True, User.is_blacklisted == False)
        elif status_filter == 'Inactive':
            query = query.filter(User.is_active == False, User.is_blacklisted == False)
        elif status_filter == 'Blacklisted':
            query = query.filter(User.is_blacklisted == True)
        elif status_filter == 'Unblacklisted':
            query = query.filter(User.is_blacklisted == False)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                db.or_(
                    Student.fname.ilike(search_term),
                    Student.lname.ilike(search_term),
                    Student.register_no.ilike(search_term)
                )
            )

        pagination = query.order_by(Student.created_at.desc()).paginate(
            page = page,
            per_page = per_page,
            error_out = False
        )

        students = []
        for student in pagination.items:
            user = User.query.get(student.user_id)
            branch_name = student.branch.branch_name
            students.append({
                "register_no": student.register_no,
                "name": f"{student.fname} {student.lname}",
                "cgpa": student.cgpa,
                "year_of_study": student.year_of_study,
                "branch": branch_name if branch_name else None,
                "is_active": user.is_active if user else False,
                "is_blacklisted": user.is_blacklisted if user else False,
                "created_at": student.created_at.isoformat()
            })

        return {
            "students": students,
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages
        }, 200
    
    @staticmethod
    def toggle_blacklist_student(register_no, blacklist):
        student = Student.query.get(register_no)
        if not student:
            return {
                "error": "Student not found"
            }, 404
        
        user = User.query.get(student.user_id)
        if not user:
            return {
                "error": "Associated user not found"
            }, 404
        
        user.is_blacklisted = blacklist
        db.session.commit()

        action = "blacklisted" if blacklist else "unblacklisted"
        logger.info(f'Student {student.fname} {student.lname}, with register no. {register_no} {action}')
        return {
            "message": f"Student {action} successfully"
        }, 200
    
    @staticmethod
    def toggle_active_student(register_no, active):
        student = Student.query.get(register_no)
        if not student:
            return {
                "error": "Student not found"
            }, 404
        
        user = User.query.get(student.user_id)
        if not user:
            return {
                "error": "Associated user not found"
            }, 404
        
        user.is_active = active
        db.session.commit()

        action = "activated" if active else "deactivated"
        logger.info(f'Student {student.fname} {student.lname}, with register no. {register_no} {action}')
        return {
            "message": f"Student {action} successfully"
        }, 200
    
    @staticmethod
    def list_all_applications(page, per_page):
        pagination = Application.query.order_by(Application.applied_date.desc()).paginate(
            page = page,
            per_page = per_page,
            error_out = False
        )

        applications = []
        for application in pagination.items:
            student = Student.query.get(application.register_no)
            drive = PlacementDrive.query.get(application.drive_id)
            company = Company.query.get(drive.company_id) if drive else None
            applications.append({
                "application_id": application.application_id,
                "register_no": application.register_no,
                "student_name": f"{student.fname} {student.lname}" if student else None,
                "drive_id": application.drive_id,
                "job_title": drive.job_title if drive else None,
                "company_name": company.company_name if company else None,
                "status": application.application_status,
                "applied_date": application.applied_date.isoformat()
            })

        return {
            "applications": applications,
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages
        }, 200
    
    @staticmethod
    def list_all_placements(page, per_page):
        pagination = Placement.query.order_by(Placement.created_at.desc()).paginate(
            page = page,
            per_page = per_page,
            error_out = False
        )

        placements = []
        for placement in pagination.items:
            application = Application.query.get(placement.application_id)
            student = Student.query.get(application.register_no)
            student_user = User.query.get(student.user_id) if student else None
            student_branch = student.branch.branch_name if student and student.branch else None
            drive = PlacementDrive.query.get(application.drive_id) if application else None
            company = Company.query.get(drive.company_id) if drive else None
            company_user = User.query.get(company.user_id) if company else None

            placements.append({
                "placement_id": placement.placement_id,
                "application_id": placement.application_id,
                "register_no": application.register_no if application else None,
                "student_name": f"{student.fname} {student.lname}" if student else None,
                "student_email": student_user.email if student_user else None,
                "student_phone": student.phone if student else None,
                "student_branch": student_branch,
                "student_cgpa": student.cgpa if student else None,
                "job_title": drive.job_title if drive else None,
                "drive_location": drive.location if drive else None,
                "company_name": company.company_name if company else None,
                "company_email": company_user.email if company_user else None,
                "company_industry": company.industry if company else None,
                "position": placement.position,
                "drive_type": placement.drive_type,
                "salary": placement.salary,
                "joining_date": placement.joining_date.isoformat() if placement.joining_date else None,
                "created_at": placement.created_at.isoformat()
            })

        return {
            "placements": placements,
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages
        }, 200
        
    @staticmethod
    def get_placement_record(placement_id):
        placement = Placement.query.get(placement_id)
        if not placement:
            return {
                "error": "Placement not found"
            }, 404
        
        application = Application.query.get(placement.application_id)            
        student = Student.query.get(application.register_no) if application else None
        branch_name = student.branch.branch_name if student else None
        drive = PlacementDrive.query.get(application.drive_id) if application else None
        company_name = Company.query(Company.company_name).get(drive.company_id) if drive else None
        user = User.query.get(student.user_id) if student else None

        return {
            "placement_id": placement.placement_id,
            "application_id": placement.application_id,
            "position": placement.position,
            "drive_type": placement.drive_type,
            "salary": placement.salary,
            "joining_date": placement.joining_date.isoformat() if placement.joining_date else None,
            "created_at": placement.created_at.isoformat(),
            "student": {
                "register_no": student.register_no,
                "student_name": f"{student.fname} {student.lname}",
                "email": user.email if user else None,
                "cgpa": student.cgpa,
                "branch": branch_name if branch_name else None,
                "year_of_study": student.year_of_study
            } if student else None,
            "drive": {
                "drive_id": drive.drive_id,
                "job_title": drive.job_title,
                "drive_type": drive.drive_type,
                "company_name": company_name if company_name else None
            } if drive else None
        }, 200