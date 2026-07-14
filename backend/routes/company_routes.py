from flask import Blueprint, request, jsonify
from utils.cache_utils import cache_response
from utils.decorators import role_required, validate_json
from services.company_service import CompanyService
from services.drive_service import DriveService
from services.application_service import ApplicationService
from services.interview_service import InterviewService

company_bp = Blueprint('company', __name__, url_prefix='/api/company')

@company_bp.route('/dashboard', methods = ['GET'])
@role_required('company')
@cache_response(key_prefix='company_dashboard')
def dashboard(current_user_id):
    result, status = CompanyService.get_dashboard(current_user_id)
    return jsonify(result), status

# ========================
# PROFILE MANAGEMENT

# 1. Get Company Profile
# 2. Update Company Profile
# =========================

@company_bp.route('/profile', methods = ['GET'])
@role_required('company')
def get_profile(current_user_id):
    result, status = CompanyService.get_profile(current_user_id)
    return jsonify(result), status

@company_bp.route('/profile', methods=['PUT'])
@role_required('company')
@validate_json()
def update_profile(current_user_id, data):
    result, status = CompanyService.update_profile(current_user_id, data)
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
def list_company_drives(current_user_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    result, status = DriveService.list_company_drives(current_user_id, page, per_page)
    return jsonify(result), status

@company_bp.route('/drives', methods = ['POST'])
@role_required('company')
@validate_json('job_title', 'job_desc', 'drive_type', 'cgpa_requirement', 'salary_max', 'application_deadline')
def create_drive(current_user_id, data):
    result, status = DriveService.create_drive(current_user_id, data)
    return jsonify(result), status

@company_bp.route('/drives/<int:drive_id>', methods = ['GET'])
@role_required('company')
def get_drive(current_user_id, drive_id):
    result, status = DriveService.get_drive(current_user_id, drive_id, role = 'company')
    return jsonify(result), status

@company_bp.route('/drives/<int:drive_id>', methods = ['PUT'])
@role_required('company')
@validate_json()
def update_drive(current_user_id, drive_id, data):
    result, status = DriveService.update_drive(current_user_id, drive_id, data)
    return jsonify(result), status

@company_bp.route('/drives/<int:drive_id>/close', methods = ['PUT'])
@role_required('company')
def close_drive(current_user_id, drive_id):
    result, status = DriveService.close_drive(current_user_id, drive_id)
    return jsonify(result), status

# ========================
# DRIVE APPLICATION MANAGEMENT

# 1. List all Applications for a Drive
# 2. Update Application Status
# =========================

@company_bp.route('/drives/<int:drive_id>/applications', methods = ['GET'])
@role_required('company')
def list_drive_applications(current_user_id, drive_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    result, status = ApplicationService.list_drive_applications(current_user_id, drive_id, page, per_page)
    return jsonify(result), status

@company_bp.route('/applications/<int:app_id>/status', methods = ['PUT'])
@role_required('company')
@validate_json('application_status')
def update_application_status(current_user_id, app_id, data):
    result, status = ApplicationService.update_application_status(current_user_id, app_id, data)
    return jsonify(result), status

# ========================
# INTERVIEW MANAGEMENT

# 1. List all Interviews for a Drive
# 2. Schedule an Interview
# 2. Update an Interview Round
# =========================

@company_bp.route('/drives/<int:drive_id>/interviews', methods = ['GET'])
@role_required('company')
def list_interviews(current_user_id, drive_id):
    result, status = InterviewService.list_interviews(current_user_id, drive_id)
    return jsonify(result), status

@company_bp.route('/drives/<int:drive_id>/interviews', methods = ['POST'])
@role_required('company')
@validate_json('round_title', 'interview_date')
def schedule_interview(current_user_id, drive_id, data):
    result, status = InterviewService.schedule_interview(current_user_id, drive_id, data)
    return jsonify(result), status

@company_bp.route('/interviews/<int:interview_id>', methods = ['PUT'])
@role_required('company')
@validate_json()
def update_interview(current_user_id, interview_id, data):
    result, status = InterviewService.update_interview(current_user_id, interview_id, data)
    return jsonify(result), status