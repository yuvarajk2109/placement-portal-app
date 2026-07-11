from flask import Blueprint, jsonify
from services.shared_service import SharedService

shared_bp = Blueprint('shared', __name__, url_prefix = '/api/shared')

@shared_bp.route('/skills', methods = ['GET'])
def list_skills():
    result, status = SharedService.list_skills()
    return jsonify(result), status

@shared_bp.route('/branches', methods = ['GET'])
def list_branches():
    result, status = SharedService.list_branches()
    return jsonify(result), status

@shared_bp.route('/drive-types', methods=['GET'])
def list_drive_types():
    result, status = SharedService.list_drive_types()
    return jsonify(result), status