from extensions import db, mail
from models.user import User
from models.student import Student
from models.company import Company
from models.placement_drive import PlacementDrive
from models.application import Application
from models.interview import Interview
from models.placement import Placement
from flask_mail import Message as MailMessage
from textwrap import dedent
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
        
        pagination = Application.query.filter_by(drive_id = drive_id).order_by(Application.created_at.desc()).paginate(
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
        new_status = data.get('application_status')
        valid_statuses = ['Shortlisted', 'Interview', 'Selected', 'Rejected']
        if new_status not in valid_statuses:
            return {
                "error": f"Invalid status. Valid statuses are: {', '.join(valid_statuses)}"
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

        if new_status == 'Interview':
            round_id = data.get('interview_round_id')
            if not round_id:
                return {
                    "error": "interview_round_id is required when setting status to 'Interview'"
                }, 400
            interview = Interview.query.get(round_id)
            if not interview or interview.drive_id != drive.drive_id:
                return {
                    "error": "Invalid interview_round_id"
                }, 400
            application.current_round_id = round_id

        if new_status =='Selected':
            existing_placement = Placement.query.filter_by(application_id  = application.application_id).first()
            if not existing_placement:
                placement = Placement(
                    application_id = application.application_id,
                    position = drive.job_title,
                    drive_type = drive.drive_type,
                    salary = drive.salary_max,
                )
                db.session.add(placement)

        db.session.commit()

        student = Student.query.get(application.register_no)
        user = User.query.get(student.user_id) if student else None
        if user:
            try:
                status_messages = {
                    'Shortlisted': f"Your have been shortlisted for {company.company_name}'s drive for the role of {drive.job_title}.",
                    'Interview': f"You have been shortlisted for an interview for {company.company_name}'s drive for the role of {drive.job_title}. Please check your dashboard for details.",
                    'Selected': f"Congratulations! You have been selected for {company.company_name}'s drive for the role of {drive.job_title}.",
                    'Rejected': f"We regret to inform you that your application for {company.company_name}'s drive for the role of {drive.job_title} has been rejected."
                }
                message = MailMessage(
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
            "message": f"Application status updated to '{new_status}"
        }, 200
                