from flask import Blueprint, jsonify
from app.utils.fetch_data import unified_data

fetch_bp = Blueprint('fetch', __name__)

@fetch_bp.route('/details', methods=['GET'])
def get_all_users():
    """
    GET endpoint to retrieve all users from the unified file.

    Returns:
        JSON: A list of user dictionaries or an empty list if file not found.
    """
    data = unified_data()
    return jsonify(data)
