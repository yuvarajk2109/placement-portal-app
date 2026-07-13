from config import Config
from extensions import db, mail
from models.user import User
from models.student import Student
from models.company import Company
from models.placement_drive import PlacementDrive
from models.application import Application
from models.interview import Interview
from models.placement import Placement
from flask_mail import Message
from textwrap import dedent
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ApplicationService:

    @staticmethod
    def list_drive_applications(user_id, drive_id, page, per_page):
        company = Company.query.filter_by(user_id = user_id).first()
        drive = PlacementDrive.query.get(drive_id)

        if not company or not drive or drive.company_id != company.company_id:
            return {
                "error": "Access denied"
            }, 403
        
        pagination = Application.query.filter(Application.drive_id == drive_id, Application.application_status != 'Inactive').order_by(Application.applied_date.desc()).paginate(
            page = page,
            per_page = per_page,
            error_out = False
        )

        applications = []
        for application in pagination.items:
            student = Student.query.get(application.register_no)
            applications.append({
                "application_id": application.application_id,
                "register_no": application.register_no,
                "student_name": f"{student.fname} {student.lname}" if student else None,
                "cgpa": student.cgpa if student else None,
                "applied_date": application.applied_date.isoformat(),
                "application_status": application.application_status,
                "current_round": application.current_round.round_title if application.current_round else None,
                "feedback": application.feedback
            })

        return {
            "applications": applications,
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages
        }, 200
    
    @staticmethod
    def update_application_status(user_id, app_id, data):
        new_status = data['application_status']
        
        if new_status not in Config.APPLICATION_ACTIONS:
            return {
                "error": f"Invalid action. Valid actions are: {', '.join(Config.APPLICATION_ACTIONS)}"
            }, 400
        
        application = Application.query.get(app_id)
        if not application:
            return {
                "error": "Application not found"
            }, 404
        
        company = Company.query.filter_by(user_id = user_id).first()
        drive = PlacementDrive.query.get(application.drive_id)
        if not company or not drive or drive.company_id != company.company_id:
            return {
                "error": "Access denied"
            }, 403
        
        application.application_status = new_status
        application.feedback = data.get('feedback', application.feedback)
        
        if new_status == 'Shortlisted':
            if application.current_round_id:
                application.current_round_id = None
                application.feedback = None

        if new_status == 'Selected for Next Round':
            if application.current_round_id is None:
                next_round = (Interview.query.filter_by(drive_id = application.drive_id).order_by(Interview.interview_id.asc()).first())
            else:
                current_round = Interview.query.get(application.current_round_id)
                next_round = (Interview.query.filter(Interview.drive_id == drive.drive_id, Interview.round_number > current_round.round_number).order_by(Interview.round_number.asc()).first())
            if next_round is None:
                new_status = "Selected"
                application.application_status = new_status
            else:
                application.current_round_id = next_round.interview_id

        if new_status == 'Selected':
            existing_placement = Placement.query.filter_by(application_id  = application.application_id).first()
            if not existing_placement:
                placement = Placement(
                    application_id = application.application_id,
                    position = drive.job_title,
                    drive_type = drive.drive_type,
                    salary = drive.salary_max,
                )
                db.session.add(placement)

                other_applications = Application.query.filter(
                    Application.register_no == application.register_no, 
                    Application.application_id != application.application_id,
                    Application.application_status.in_(['Applied', 'Shortlisted', 'Interview'])
                ).all()
                for application in other_applications:
                    application.application_status = 'Withdrawn'
                    application.feedback = 'Automatically withdrawn due to placement being secured in another drive.'


        db.session.commit()

        student = Student.query.get(application.register_no)
        user = User.query.get(student.user_id) if student else None
        if user:
            try:
                status_messages = {
                    'Shortlisted': f"Your have been shortlisted for {company.company_name}'s drive for the role of {drive.job_title}.",
                    'Selected for Next Round': f"You have been selected for an interview for {company.company_name}'s drive for the role of {drive.job_title}. Please check your dashboard for details.",
                    'Selected': f"Congratulations! You have been selected for {company.company_name}'s drive for the role of {drive.job_title}.",
                    'Rejected': f"We regret to inform you that your application for {company.company_name}'s drive for the role of {drive.job_title} has been rejected."
                }
                message = Message(
                    subject = f"Placement Portal - Application Update: {drive.job_title} at {company.company_name}",
                    recipients = [user.email],
                    body = dedent(
f"""
Dear {student.fname},
{status_messages.get(new_status, "Your application status has been updated.")}
Company: {company.company_name}
Role: {drive.job_title}
Feedback: {application.feedback or 'N/A'}

Regards,
Placement Portal Team
"""
                    )
                )
                mail.send(message)
            except Exception as e:
                logger.warning(f"Could not send status notification to {user.email}: {e}")

        return  {
            "message": f"Application status updated to '{new_status}'"
        }, 200
                
    @staticmethod
    def apply_for_drive(user_id, drive_id):
        student = Student.query.filter_by(user_id = user_id).first()
        if not student:
            return {
                "error": "Student not found"
            }, 404
        
        drive =  PlacementDrive.query.get(drive_id)
        if not drive:
            return {
                "error": "Placement drive not found"
            }, 404
        
        if drive.status != 'Approved':
            return {
                "error": "This drive is not open for applications"
            }, 403
        
        if datetime.now() > drive.application_deadline:
            return {
                "error": "Application deadline has passed"
            }, 400
        
        if student.cgpa < drive.cgpa_requirement:
            return {
                "error": f"Minimum CGPA requirement for this drive is {drive.cgpa_requirement}"
            }, 400
        
        if student.year_of_study == 3 and drive.drive_type != '2M Internship':
            return {
                "error": "Year 3 students can only apply for 2-month internship drives."
            }, 400
        
        if student.year_of_study == 4 and drive.drive_type == '2M Internship':
            return {
                "error": "Year 4 students can't apply for 2-month internship drives."
            }, 400
        
        if student.branch not in drive.eligible_branches:
            return {
                "error": f"{student.branch.branch_name} students are not eligible for this drive."
            }, 403
        
        is_placed = Placement.query.join(Application).filter(Application.register_no == student.register_no).first()
        if is_placed:
            return {
                "error": "You've already been placed and can't apply for new drives"
            }, 403
        
        existing = Application.query.filter(
            Application.register_no == student.register_no, 
            Application.drive_id == drive.drive_id,
            Application.application_status != 'Inactive').first()
        if existing:
            return {
                "error": "You have already applied for this drive"
            }, 409
        
        application = Application(
            register_no = student.register_no,
            drive_id = drive_id,
            application_status = 'Applied'
        )
        db.session.add(application)
        db.session.commit()

        company = Company.query.filter_by(company_id = drive.company_id).first()

        logger.info(f"Student {student.fname} {student.lname} ({student.register_no}) has applied for drive {drive_id} - {drive.job_title} by {company.company_name}")
        return {
            "message": "Application submitted successfully",
            "application_id": application.application_id
        }, 201
    
    @staticmethod
    def list_student_applications(user_id, page, per_page):
        student = Student.query.filter_by(user_id = user_id).first()
        if not student:
            return {
                "error": "Student not found"
            }, 404
        
        pagination = Application.query.filter_by(register_no = student.register_no).order_by(Application.applied_date.desc()).paginate(
            page = page,
            per_page = per_page,
            error_out = False
        )
        
        applications = []
        for application in pagination.items:
            drive = PlacementDrive.query.get(application.drive_id)
            company = Company.query.get(drive.company_id) if drive else None
            applications.append({
                "application_id": application.application_id,
                "drive_id": application.drive_id,
                "job_title": drive.job_title if drive else None,
                "company_name": company.company_name if company else None,
                "applied_date": application.applied_date.isoformat(),
                "status": application.application_status,
                "feedback": application.feedback
            })

        return {
            "applications": applications,
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages
        }, 200
    
    @staticmethod
    def get_student_application_details(user_id, application_id):
        student = Student.query.filter_by(user_id = user_id).first()
        application = Application.query.get(application_id)
        
        if not application or application.register_no != student.register_no:
            return {
                "error": "Application not found"
            }, 403
        
        drive = PlacementDrive.query.get(application.drive_id)
        company = Company.query.get(drive.company_id) if drive else None

        return {
            "application_id": application.application_id,
            "drive_id": application.drive_id,
            "job_title": drive.job_title if drive else None,
            "job_desc": drive.job_desc if drive else None,
            "salary_min": drive.salary_min if drive else None,
            "salary_max": drive.salary_max if drive else None,
            "location": drive.location if drive else None,
            "company_name": company.company_name if company else None,
            "applied_date": application.applied_date.isoformat(),
            "status": application.application_status,
            "feedback": application.feedback,
            "current_round_id": application.current_round_id,
            "current_round_number": application.current_round.round_number if application.current_round else None,
            "current_round_title": application.current_round.round_title if application.current_round else None,
            "current_round_location": application.current_round.location if application.current_round else None
        }, 200
    
    @staticmethod
    def withdraw_application(user_id, application_id):
        student = Student.query.filter_by(user_id = user_id).first()
        application = Application.query.get(application_id)

        if not application or application.register_no != student.register_no:
            return {
                "error": "Application not found"
            }, 403
        
        if application.application_status not in ('Applied', 'Shortlisted'):
            return {
                "error": "Cannot withdraw. Application has progressed beyond initial stages."
            }, 400
        
        application.application_status = 'Withdrawn'
        db.session.commit()
        return {
            "message": "Application withdrawn successfully"
        }, 200
        

        
        