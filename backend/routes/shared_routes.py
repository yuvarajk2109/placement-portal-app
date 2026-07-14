from flask import Blueprint, jsonify
from utils.cache_utils import cache_response
from services.shared_service import SharedService

shared_bp = Blueprint('shared', __name__, url_prefix = '/api/shared')

@shared_bp.route('/skills', methods = ['GET'])
@cache_response(ttl = 1200, key_prefix='skills')
def list_skills():
    result, status = SharedService.list_skills()
    return jsonify(result), status

@shared_bp.route('/branches', methods = ['GET'])
@cache_response(ttl = 1200, key_prefix='branches')
def list_branches():
    result, status = SharedService.list_branches()
    return jsonify(result), status

@shared_bp.route('/drive-types', methods=['GET'])
@cache_response(ttl = 1200, key_prefix='drive_types')
def list_drive_types():
    result, status = SharedService.list_drive_types()
    return jsonify(result), status

@shared_bp.route('/application-statuses', methods=['GET'])
@cache_response(ttl = 1200, key_prefix='application_statuses')
def list_application_statuses():
    result, status = SharedService.list_application_statuses()
    return jsonify(result), status

@shared_bp.route('/application-actions', methods=['GET'])
@cache_response(ttl = 1200, key_prefix='application_actions')
def list_application_actions():
    result, status = SharedService.list_application_actions()
    return jsonify(result), status

@shared_bp.route('/dashboard', methods=['GET'])
@cache_response(ttl = 1200, key_prefix='home_dashboard')
def get_dashboard():
    result, status = SharedService.get_dashboard()
    return jsonify(result), status