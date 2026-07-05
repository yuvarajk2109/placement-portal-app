from flask import Blueprint, request, jsonify
from utils.decorators import role_required, validate_json
from services.admin_service import AdminService

admin_bp = Blueprint('admin', __name__, url_prefix = '/api/admin')

@admin_bp.route('/dashboard', methods = ['GET'])
@role_required('admin')
def dashboard():
    result, status = AdminService.get_dashboard()
    return jsonify(result), status

# ==================
# COMPANY MANAGEMENT

# 1. List All Companies
# 2. Approve a Company
# 3. Reject a Company
# 4. Remove a Company
# 5. Blacklist a Company
# 6. Unblacklist a Company
# ==================

@admin_bp.route('/companies', methods = ['GET'])
@role_required('admin')
def list_companies():
    status_filter = request.args.get('status')
    search = request.args.get('search')
    page = request.args.get('page', 1, type = int)
    per_page = request.args.get('per_page', 20, type = int)
    result, status = AdminService.list_companies(status_filter, search, page, per_page)
    return jsonify(result), status

@admin_bp.route('/companies/<int:company_id>/approve', methods = ['PUT'])
@role_required('admin')
def approve_company(company_id):
    result, status = AdminService.update_company_status(company_id, 'Approved')
    return jsonify(result), status

@admin_bp.route('/companies/<int:company_id>/reject', methods = ['PUT'])
@role_required('admin')
def reject_company(company_id):
    result, status = AdminService.update_company_status(company_id, 'Rejected')
    return jsonify(result), status

@admin_bp.route('/companies/<int:company_id>', methods = ['DELETE'])
@role_required('admin')
def remove_company(company_id):
    result, status = AdminService.remove_company(company_id)
    return jsonify(result), status

@admin_bp.route('/companies/<int:company_id>/blacklist', methods = ['PUT'])
@role_required('admin')
def blacklist_company(company_id):
    result, status = AdminService.toggle_blacklist_company(company_id, blacklist = True)
    return jsonify(result), status

@admin_bp.route('/companies/<int:company_id>/unblacklist', methods = ['PUT'])
@role_required('admin')
def unblacklist_company(company_id):
    result, status = AdminService.toggle_blacklist_company(company_id, blacklist = False)
    return jsonify(result), status

# =================
# DRIVE MANAGEMENT

# 1. List All Drives
# 2. Approve a Drive
# 3. Reject a Drive
# =================

@admin_bp.route('/drives', methods = ['GET'])
@role_required('admin')
def list_drives():
    status_filter = request.args.get('status')
    page = request.args.get('page', 1, type = int)
    per_page = request.args.get('per_page', 20, type = int)
    result, status = AdminService.list_drives(status_filter, page, per_page)
    return jsonify(result), status

@admin_bp.route('/drives/<int:drive_id>/approve', methods = ['PUT'])
@role_required('admin')
def approve_drive(drive_id):
    result, status = AdminService.update_drive_status(drive_id, 'Approved')
    return jsonify(result), status

@admin_bp.route('/drives/<int:drive_id>/reject', methods = ['PUT'])
@role_required('admin')
def reject_drive(drive_id):
    result, status = AdminService.update_drive_status(drive_id, 'Rejected')
    return jsonify(result), status

# ==================
# STUDENT MANAGEMENT

# 1. List all Students
# 2. Blacklist Student
# 3. Unblacklist Student
# 4. Deactivate Student Account
# 5. Reactivate Student Account
# ==================

@admin_bp.route('/students', methods = ['GET'])
@role_required('admin')
def list_students():
    search = request.args.get('search')
    page = request.args.get('page', 1, type = int)
    per_page = request.args.get('per_page', 20, type = int)
    result, status = AdminService.list_students(search, page, per_page)
    return jsonify(result), status

@admin_bp.route('/students/<string:register_no>/blacklist', methods = ['PUT'])
@role_required('admin')
def blacklist_student(register_no):
    result, status = AdminService.toggle_blacklist_student(register_no, blacklist = True)
    return jsonify(result), status

@admin_bp.route('/students/<string:register_no>/unblacklist', methods = ['PUT'])
@role_required('admin')
def unblacklist_student(register_no):
    result, status = AdminService.toggle_blacklist_student(register_no, blacklist = False)
    return jsonify(result), status

@admin_bp.route('/students/<string:register_no>/deactivate', methods = ['PUT'])
@role_required('admin')
def deactivate_student(register_no):
    result, status = AdminService.toggle_active_student(register_no, active = False)
    return jsonify(result), status

@admin_bp.route('/students/<string:register_no>/activate', methods = ['PUT'])
@role_required('admin')
def activate_student(register_no):
    result, status = AdminService.toggle_active_student(register_no, active = True)
    return jsonify(result), status

# ==================
# SKILL MANAGEMENT

# 1. Create New Skill
# 2. Delete a Skill
# ==================

@admin_bp.route('/skills', methods = ['POST'])
@role_required('admin')
@validate_json('skill_name')
def create_skill(data):
    result, status = AdminService.create_skill(data)
    return jsonify(result), status

@admin_bp.route('/skills/<int:skill_id>', methods = ['DELETE'])
@role_required('admin')
def delete_skill(skill_id):
    result, status = AdminService.delete_skill(skill_id)
    return jsonify(result), status

# ==================
# APPLICATIONS MANAGEMENT

# 1. List All Applications
# ==================

@admin_bp.route('/applications', methods = ['GET'])
@role_required('admin')
def list_all_applications():
    page = request.args.get('page', 1, type = int)
    per_page = request.args.get('per_page', 20, type = int)
    result, status = AdminService.list_all_applications(page, per_page)
    return jsonify(result), status

# ==================
# PLACEMENT MANAGEMENT

# 1. List All Placements
# 2. View Specific Placement Details
# ==================

@admin_bp.route('/placements', methods = ['GET'])
@role_required('admin')
def list_all_placements():
    page = request.args.get('page', 1, type = int)
    per_page = request.args.get('per_page', 20, type = int)
    result, status = AdminService.list_all_placements(page, per_page)
    return jsonify(result), status

@admin_bp.route('/placements/<int:placement_id>', methods = ['GET'])
@role_required('admin')
def get_placement_record(placement_id):
    result, status = AdminService.get_placement_record(placement_id)
    return jsonify(result), status