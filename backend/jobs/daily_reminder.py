import logging
from config import Config
from datetime import date, timedelta
from extensions import mail
from flask_mail import Message
from models.application import Application
from models.placement_drive import PlacementDrive
from models.student import Student
from models.user import User
from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task(name = "jobs.daily_reminder.send_daily_reminders")
def send_daily_reminders():
    upcoming_date = date.today() + timedelta(days = Config.DAILY_REMINDER_DEADLINE)
    drives = PlacementDrive.query.filter(
        PlacementDrive.status == 'Approved', 
        PlacementDrive.application_deadline <= upcoming_date,
        PlacementDrive.application_deadline >= date.today()).all()
    
    if not drives:
        logger.info(f"[REMINDER] No upcoming deadlines (with deadline in {Config.DAILY_REMINDER_DEADLINE} days)")
        return "No reminders"

    students = Student.query.join(User).filter(
        User.is_active == True,
        User.is_blacklisted == False,
        User.is_verified == True
    ).all()

    count = 0
    for student in students:
        user = User.query.get(student.user_id)
        eligible_drives = []

        for drive in drives:
            if student.year_of_study == 3 and drive.drive_type != '2M Internship':
                continue
            if student.year_of_study == 4 and drive.drive_type == '2M Internship':
                continue

        already_applied = Application.query.filter(
            Application.register_no == student.register_no, 
            Application.drive_id == drive.drive_id,
            Application.application_status != 'Inactive').first()
    
        if not already_applied and student.cgpa >= drive.cgpa_requirement:
            eligible_drives.append(drive)

        if eligible_drives:
            drive_list = "\n".join(
                f" - {drive.job_title} (Deadline: {drive.application_deadline.strftime('%Y-%m-%d %H:%M')})""
                for drive in eligible_drives
            )
            try:
                message = Message(
                    subject = "Placement Portal - Upcoming Drive Application Deadline Reminder",
                    recipients = [user.email],
                    body = (
f'''
Hello, {student.fname},

The following placement drives have upcoming deadlines:

{drive_list}

Apply to the drives as soon as possible if you are interested.

Regards,
Placement Portal Team
'''
                    )
                )
                mail.send(message)
                count += 1
            except Exception as e:
                logger.error(f"Failed to send reminder to {user.email}: {e}")
    logger.info(f"[REMINDER] Sent reminders to {count} students.")
    return f"Sent {count} reminders"
        
