from flask import Blueprint, request, jsonify
from utils.decorators import role_required, validate_json
from services.student_service import StudentService
from services.application_service import ApplicationService
from jobs.export_csv import export_applications_csv

student_bp = Blueprint('student', __name__, url_prefix = '/api/student')

@student_bp.route('/dashboard', methods = ['GET'])
@role_required('student')
def dashboard(current_user_id):
    result, status = StudentService.get_dashboard(current_user_id)
    return jsonify(result), status

# =========================
# PROFILE MANAGEMENT

# 1. Get Profile Details
# 2. Update Profile Details
# =========================

@student_bp.route('/profile', methods = ['GET'])
@role_required('student')
def get_profile(current_user_id):
    result, status = StudentService.get_profile(current_user_id)
    return jsonify(result), status

@student_bp.route('/profile', methods = ['PUT'])
@role_required('student')
@validate_json()
def update_profile(current_user_id, data):
    result, status = StudentService.update_profile(current_user_id, data)
    return jsonify(result), status

# ==================
# RESUME MANAGEMENT

# 1. Upload Resume
# 2. Download Resume
# ==================

@student_bp.route('/resume', methods = ['POST'])
@role_required('student')
def upload_resume(current_user_id):
    if 'resume' not in request.files:
        return jsonify({
            "error": "No resume file provided"
        }), 400
    
    resume = request.files['resume']
    result, status = StudentService.upload_resume(current_user_id, resume)
    return jsonify(result), status

@student_bp.route('/resume', methods = ['GET'])
@role_required('student')
def download_resume(current_user_id):
    return StudentService.download_resume(current_user_id)

# ===============================
# DRIVE MANAGEMENT

# 1. List Available Drives
# 2. Get Specific Drive's Details
# ================================

@student_bp.route('/drives', methods = ['GET'])
@role_required('student')
def list_eligible_drives(current_user_id):
    search = request.args.get('search')
    location = request.args.get('location')
    drive_type = request.args.get('drive_type')
    min_salary = request.args.get('min_salary', type = float)
    application_status = request.args.get('application_status')
    page = request.args.get('page', 1, type = int)
    per_page = request.args.get('per_page', 20, type = int)
    result, status = StudentService.list_eligible_drives(current_user_id, search, location, drive_type, min_salary, application_status, page, per_page)
    return jsonify(result), status

@student_bp.route('/drives/<int:drive_id>', methods = ['GET'])
@role_required('student')
def get_drive_details(current_user_id, drive_id):
    result, status = StudentService.get_drive_details(current_user_id, drive_id)
    return jsonify(result), status

# ===============================
# APPLICATION MANAGEMENT

# 1. Apply for a Drive
# 2. List Student's Applications
# 3. View Specific Applicaton's Detail
# 4. Withdraw Application
# ================================

@student_bp.route('/drives/<int:drive_id>/apply', methods = ['POST'])
@role_required('student')
def apply_for_drive(current_user_id, drive_id):
    result, status = ApplicationService.apply_for_drive(current_user_id, drive_id)
    return jsonify(result), status

@student_bp.route('/applications', methods = ['GET'])
@role_required('student')
def list_my_applications(current_user_id):
    page = request.args.get('page', 1, type = int)
    per_page = request.args.get('per_page', 20, type = int)
    result, status = ApplicationService.list_student_applications(current_user_id, page, per_page)
    return jsonify(result), status

@student_bp.route('/applications/<int:app_id>', methods = ['GET'])
@role_required('student')
def get_application_detail(current_user_id, app_id):
    result, status = ApplicationService.get_student_application_details(current_user_id, app_id)
    return jsonify(result), status

@student_bp.route('/applications/<int:app_id>/withdraw', methods = ['PUT'])
@role_required('student')
def withdraw_application(current_user_id, app_id):
    result, status = ApplicationService.withdraw_application(current_user_id, app_id)
    return jsonify(result), status

# ===============================
# PLACEMENT MANAGEMENT

# 1. View Placement
# ================================

@student_bp.route('/placement', methods = ['GET'])
@role_required('student')
def get_placement(current_user_id):
    result, status = StudentService.get_placement(current_user_id)
    return jsonify(result), status

# ===============================
# EXPORTS MANAGEMENT

# 1. Export Applications
# ================================

@student_bp.route('/export/applications', methods = ['POST'])
@role_required('student')
def export_applications(current_user_id):
    export_applications_csv.delay(current_user_id)
    return jsonify({
        "message": "Export has begun. You'll receive the CSV to your university email address."
    }), 202