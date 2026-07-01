from extensions import db
from models.company import Company
from models.placement_drive import PlacementDrive
from models.application import Application
import logging

logger = logging.getLogger(__name__)

class CompanyService:

    @staticmethod
    def get_dashboard(user_id):
        company = Company.query.filter_by(user_id= user_id).first()
        if not company:
            return {
                "error": "Company not found"
            }, 404
        
        drives = PlacementDrive.query.filter_by(company_id = company.company_id).all()
        drive_ids = [drive.drive_id for drive in drives]

        total_drives = len(drives)
        active_drives = sum(1 for drive in drives if drive.status == 'Active')
        pending_drives = sum(1 for drive in drives if drive.status == 'Pending')

        total_applications = Application.query.filter(Application.drive_id .in_(drive_ids)).count() if drive_ids else 0
        total_selected = Application.query.filter(Application.drive_id.in_(drive_ids), Application.application_status == 'Selected').count() if drive_ids else 0

        return {
            "company_name": company.company_name,
            "status": company.status,
            "total_drives": total_drives,
            "active_drives": active_drives,
            "pending_drives": pending_drives,
            "total_applications": total_applications, 
            "total_selected": total_selected
        }, 200


    @staticmethod
    def get_profile(user_id):
        company = Company.query.filter_by(user_id= user_id).first()
        if not company:
            return {
                "error": "Company not found"
            }, 404
        
        return {
            "company_id": company.company_id,
            "company_name": company.company_name,
            "industry": company.industry,
            "website": company.website,
            "description": company.description,
            "hr_name": company.hr_name,
            "hr_email": company.hr_email,
            "hr_phone": company.hr_phone,
            "status": company.status,
            "created_at": company.created_at.isoformat()
        }, 200
    
    @staticmethod
    def update_profile(user_id, data):
        company = Company.query.filter_by(user_id = user_id).first()
        if not company:
            return {
                "error": "Company not found"
            }
        
        updatable = [
            'company_name',
            'industry',
            'website',
            'location',
            'description',
            'hr_name',
            'hr_email',
            'hr_phone'
        ]

        for field in updatable:
            if field in data:
                setattr(company, field, data[field])

        db.session.commit()
        logger.info(f"Company '{company.company_name}' profile updated successfully.")
        return {
            "message": "Profile updated successfully"
        }, 200