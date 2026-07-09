from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils.decorators import role_required, validate_json
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix = '/api/auth')

@auth_bp.route('/register/student', methods = ['POST'])
@validate_json('email', 'password', 'register_no', 'fname', 'lname', 'dob', 'cgpa', 'branch_id')
def register_student(data):
    result, status_code = AuthService.register_student(data)
    return jsonify(result), status_code

@auth_bp.route('/verify-otp', methods = ['POST'])
@validate_json('email', 'otp')
def verify_otp(data):
    result, status_code = AuthService.verify_otp(data)
    return jsonify(result), status_code

@auth_bp.route('/resend-otp', methods = ['POST'])
@validate_json('email')
def resend_otp(data):
    result, status_code = AuthService.resend_otp(data)
    return jsonify(result), status_code

@auth_bp.route('/register/company', methods = ['POST'])
@validate_json('email', 'password', 'company_name', 'hr_email')
def register_company(data):
    result, status_code = AuthService.register_company(data)
    return jsonify(result), status_code

@auth_bp.route('/login', methods = ['POST'])
@validate_json('email', 'password')
def login(data):
    result, status_code = AuthService.login(data)
    return jsonify(result), status_code

@auth_bp.route('/refresh', methods = ['POST'])
@jwt_required(refresh = True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity = str(user_id))
    return jsonify({
        "access_token": access_token
    }), 200

@auth_bp.route('/profile', methods = ['GET'])
@role_required()
@jwt_required()
def get_current_user(current_user_id):
    result, status_code = AuthService.get_current_user(current_user_id)
    return jsonify(result), status_code