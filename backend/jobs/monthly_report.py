import logging
from config import Config
from datetime import date, timedelta
from flask import render_template
from flask_mail import Message
from extensions import mail
from models.user import User
from models.application import Application
from models.placement import Placement
from models.placement_drive import PlacementDrive
from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task(name = "jobs.monthly_report.generate_monthly_report")
def generate_monthly_report():
    today = date.today()
    current_month_start = today.replace(day = Config.MONTHLY_REPORT_DAY)
    previous_month_end = current_month_start - timedelta(days = Config.MONTHLY_REPORT_DAY)
    previous_month_start = previous_month_end.replace(day = Config.MONTHLY_REPORT_DAY)

    total_drives_count = PlacementDrive.query.filter(
        PlacementDrive.created_at >= previous_month_start,
        PlacementDrive.created_at <= current_month_start,
    ).count()

    approved_drives_count = PlacementDrive.query.filter(
        PlacementDrive.created_at >= previous_month_start,
        PlacementDrive.created_at <= current_month_start,
        PlacementDrive.status == 'Approved'
    ).count()

    total_applications_count = Application.query.filter(
        Application.applied_date >= previous_month_start,
        Application.applied_date <= previous_month_end
    ).count()

    active_applications_count = Application.query.filter(
        Application.applied_date >= previous_month_start,
        Application.applied_date <= previous_month_end,
        Application.application_status != 'Inactive'
    ).count()

    placements_count = Placement.query.filter(
        Placement.created_at <= previous_month_start,
        Placement.created_at >= previous_month_end
    )

    report = {
         'time_period': f"{previous_month_start.strftime('%d %B %Y') - {current_month_start.strftime('%d %B %Y')}}",
         'total_drives_count': total_drives_count,
         'approved_drives_count': approved_drives_count,
         'total_applications_count': total_applications_count,
         'active_applications_count': active_applications_count,
         'placements_count': placements_count,
         'generated_on': today.isoformat()
    }

    html_content = render_template('monthly_report.html', **report)

    admin = User.query.filter_by(role='admin').first()
    if admin:
        try:
            message = Message(
                subject = f"Placement Portal - Monthly Report ({report['time_period']})",
                recipients = [admin.email],
                html = html_content
            )
            mail.send(message)
            logger.info("[REPORT] Monthly report sent to", {admin.email})
        except Exception as e:
            logger.error("Failed to send monthly report:", e)
    return report