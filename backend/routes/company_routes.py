from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from utils.decorators import role_required, validate_json
from services.company_service import CompanyService
from services.drive_service import DriveService
from services.application_service import ApplicationService
from services.interview_service import InterviewService

company_bp = Blueprint('company', __name__, url_prefix='/api/company')

@company_bp.route('/dashboard', methods = ['GET'])
@role_required('company')
def dashboard():
    user_id = get_jwt_identity()
    data = request.get_json()
    result, status = DriveService.create_drive(user_id, data)
    return jsonify(result), status

# ========================
# PROFILE MANAGEMENT

# 1. Get Company Profile
# 2. Update Company Profile
# =========================

@company_bp.route('/profile', methods = ['GET'])
@role_required('company')
def get_profile():
    user_id = get_jwt_identity()
    result, status = CompanyService.get_profile(user_id)
    return jsonify(result), status

@company_bp.route('/profile', methods=['PUT'])
@role_required('company')
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()
    result, status = CompanyService.update_profile(user_id, data)
    return jsonify(result), status

# ========================
# DRIVE MANAGEMENT

# 1. Get Company Drives
# 2. Create a Drive
# 3. Get Drive Details
# 4. Update Drive Details
# 5. Close a Drive
# =========================

@company_bp.route('/drives', methods = ['GET'])
@role_required('company')
def list_company_drives():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    result, status = DriveService.list_company_drives(user_id, page, per_page)
    return jsonify(result), status

@company_bp.route('/drives', methods = ['POST'])
@role_required('company')
@validate_json('job_title', 'job_desc', 'drive_type', 'cgpa_requirement', 'salary_max', 'application_deadline')
def create_drive():
    user_id = get_jwt_identity()
    data = request.get_json()
    result, status = DriveService.create_drive(user_id, data)
    return jsonify(result), status

@company_bp.route('/drives/<int:drive_id>', methods = ['GET'])
@role_required('company')
def get_drive(drive_id):
    user_id = get_jwt_identity()
    result, status = DriveService.get_drive(user_id, drive_id, role = 'company')
    return jsonify(result), status

@company_bp.route('/drives/<int:drive_id>', methods = ['PUT'])
@role_required('company')
def update_drive(drive_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    result, status = DriveService.update_drive(user_id, drive_id, data)
    return jsonify(result), status

@company_bp.route('/drives/<int:drive_id>/close', methods = ['PUT'])
@role_required('company')
def close_drive(drive_id):
    user_id = get_jwt_identity()
    result, status = DriveService.close_drive(user_id, drive_id)
    return jsonify(result), status

# ========================
# DRIVE APPLICATION MANAGEMENT

# 1. List all Applications for a Drive
# 2. Update Application Status
# =========================

@company_bp.route('/drives/<int:drive_id/applications', methods = ['GET'])
@role_required('company')
def list_drive_applications(drive_id):
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    result, status = ApplicationService.list_drive_applications(user_id, drive_id, page, per_page)
    return jsonify(result), status

@company_bp.route('/drives/<int:app_id>/status/', methods = ['PUT'])
@role_required('company')
def update_application_status(app_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    result, status = ApplicationService.update_application_status(user_id, app_id, data)
    return jsonify(result), status

# ========================
# INTERVIEW MANAGEMENT

# 1. List all Interviews for a Drive
# 2. Schedule an Interview
# 2. Update an Interview Round
# =========================

@company_bp.route('/drives/<int:drive_id>/interviews', methods = ['GET'])
@role_required('company')
def list_interviews(drive_id):
    user_id = get_jwt_identity()
    result, status = InterviewService.list_interviews(user_id, drive_id)
    return jsonify(result), status

@company_bp.route('/drives/<int:drive_id>/interviews', methods = ['POST'])
@role_required('company')
@validate_json('round_title', 'interview_date')
def schedule_interview(drive_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    result, status = InterviewService.schedule_interview(user_id, drive_id, data)
    return jsonify(result), status

@company_bp.route('/interviews/<int:interview_id>', methods = ['PUT'])
@role_required('company')
def update_interview(interview_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    result, status = InterviewService.update_interview(user_id, interview_id, data)
    return jsonify(result), status