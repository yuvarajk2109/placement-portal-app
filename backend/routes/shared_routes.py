from flask import Blueprint, request, jsonify
from services.shared_service import SharedService

shared_bp = Blueprint('shared', __name__, url_prefix = '/api/shared')

@shared_bp.route('/skills', methods = ['GET'])
def list_skills():
    result, status = SharedService.list_skills()
    return jsonify(result), status