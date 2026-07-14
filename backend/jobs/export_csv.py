import logging
import csv
import os
from datetime import datetime
from extensions import mail
from config import Config
from models.student import Student
from models.user import User
from models.company import Company
from models.placement_drive import PlacementDrive
from models.application import Application
from flask_mail import Message
from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task(name = "jobs.export_csv.export_applications_csv")
def export_applications_csv(user_id):
    os.makedirs(Config.EXPORT_FOLDER, exist_ok = True)
    
    student = Student.query.filter_by(user_id = user_id).first()
    if not student:
        logger.error(f"Student not found with user_id = {user_id}")
        return "Student not found"
    
    user = User.query.get(user_id)
    applications = Application.query.filter_by(register_no = student.register_no).order_by(Application.applied_date.desc()).all()

    timestamp = datetime.now().strftime("%d_%m_%Y__%H_%M_%S")
    file_name = f"applications_{student.register_no}_{timestamp}.csv"
    file_path = os.path.join(Config.EXPORT_FOLDER, file_name)
    

    with open(file_path, 'w', newline = '', encoding = "utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([
            'Register No',
            'Company Name',
            'Job Title',
            'Drive Type',
            'Application Status',
            'Feedback',
            'Applied Date',
            'Updated At'
        ])
        for application in applications:
            drive = PlacementDrive.query.get(application.drive_id)
            company = Company.query.get(drive.company_id) if drive else None
            writer.writerow([
                student.register_no,
                company.company_name if company else 'N/A',
                drive.job_title if drive else 'N/A',
                drive.drive_type if drive else 'N/A',
                application.application_status,
                application.feedback,
                application.applied_date.isoformat() if application.applied_date else '',
                application.updated_at.isoformat() if application.updated_at else ''
            ])

    try:
        message = Message(
            subject = "Placement Portal - Application Export is Ready",
            recipients = [user.email],
            body = (
f'''
Hi {student.fname},

Your application history export is ready and attached to this email.

Regards,
Placement Portal Team'''
            )
        )
        with open(file_path, 'rb') as f:
            message.attach(file_name, 'text/csv', f.read())
        mail.send(message)
        logger.info(f"[EXPORT] Applications CSV sent to {user.email}; CSV size = {os.path.getsize(file_path)} bytes")
    except Exception as e:
        logger.error(f"Failed to send CSV export: {e}")

    return {
        "file": file_name,
        "status": "completed"
    }