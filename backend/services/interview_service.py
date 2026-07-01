from extensions import db
from models.company import Company
from models.placement_drive import PlacementDrive
from models.interview import Interview
from datetime import datetime
import logging


logger = logging.getLogger(__name__)

class InterviewService:

    @staticmethod
    def schedule_interview(user_id, drive_id, data):
        company = Company.query.filter_by(user_id = user_id).first()
        drive = PlacementDrive.query.get(drive_id)

        if not company or not drive or drive.company_id != company.company_id:
            return {
                "error": "Access denied"
            }, 403
        
        existing_rounds = Interview.query.filter_by(drive_id = drive_id).count()
        round_number = existing_rounds + 1
        
        try:
            interview_date = datetime.fromisoformat(data['interview_date'])
        except ValueError:
            return {
                "error": "Invalid interview date format. Use ISO format"
            }, 400
        
        interview = Interview(
            drive_id = drive_id,
            round_number = round_number,
            round_title = data['round_title'],
            interview_date = interview_date,
            location = data.get('location')
        )
        db.session.add(interview)
        db.session.commit()

        logger.info(
            f"Interview round '{data['round_title']} (round {round_number}) scheduled for the role of {drive.job_title} by company {company.company_name}"
        )

        return {
            "message": "Interview round scheduled",
            "interview_id": interview.interview_id,
            "round_number": interview.round_number
        }, 201
    
    @staticmethod
    def list_interviews(user_id, drive_id):
        company = Company.query.filter_by(user_id = user_id).first()
        drive = PlacementDrive.query.get(drive_id)

        if not company or not drive or drive.company_id != company.company_id:
            return {
                "error": "Access denied"
            }, 403
        
        interviews = Interview.query.filter_by(drive_id = drive_id).order_by(Interview.round_number).all()

        return {
            "interviews": [
                {
                    "interview_id": interview.interview_id,
                    "round_number": interview.round_number,
                    "round_title": interview.round_title,
                    "interview_date": interview.interview_date.isoformat() if interview.interview_date else None,
                    "location": interview.location,
                    "created_at": interview.created_at.isoformat()
                }
            ]
            for interview in interviews
        }, 200
    
    @staticmethod
    def update_interview(user_id, interview_id, data):
        interview = Interview.query.get(interview_id)
        if not interview:
            return {
                "error": "Interview not found"
            }, 404
        
        drive = PlacementDrive.query.get(interview.drive_id)
        company = Company.query.filter_by(user_id = user_id).first()

        if not company or not drive or drive.company_id != company.company_id:
            return {
                "error": "Access denied"
            }, 403
        
        if 'round_title' in data:
            interview.round_title = data['round_title']
        if 'location' in data:
            interview.location = data['location']
        if 'interview_date' in data:
            try:
                interview.interview_date = datetime.fromisoformat(data['interview_date'])
            except ValueError:
                return {
                    "error": "Invalid interview date format. Use ISO format"
                }, 400
            
        db.session.commit()
        logger.info(f"Interview {interview_id} by {company.company_name} for {drive.job_title} updated")

        return {
            "message": "Interview updated successfully"
        }, 200