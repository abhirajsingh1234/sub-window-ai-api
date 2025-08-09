from flask import Blueprint, jsonify, request
from app.utils.handler import handle_action

Add_Del_bp = Blueprint('add_del', __name__)

@Add_Del_bp.route('/', methods=['GET'])
def get_route():
    """
    Handle GET request to indicate usage instruction.
    
    Returns:
        JSON response suggesting to use POST instead.
    """
    return jsonify({'message': 'Please use POST method with action, name, contact, mail id'})

@Add_Del_bp.route('/', methods=['POST'])
def post_route():
    """
    Handle POST request for add/update/delete actions on contact and mail data.

    Expects JSON body with keys:
        - action: 'add', 'update', or 'delete'
        - name (optional): name of user
        - contact (optional): contact number
        - mail_id (optional): email address
    
    Returns:
        JSON response based on action performed.
    """
    data = request.get_json(force=True)

    action = data.get('action')
    name = data.get('name')
    contact = data.get('contact')
    mail_id = data.get('mail_id')

    if not action:
        return jsonify({'error': 'Missing action'}), 400

    result = handle_action(action, name, contact, mail_id)
    return jsonify(result)
