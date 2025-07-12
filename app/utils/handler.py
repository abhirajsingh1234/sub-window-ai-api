from app.utils.add_user import add_user
from app.utils.update_user import update_user
from app.utils.delete_user import delete_user

def handle_action(action, name=None, contact=None, mail_id=None):
    """
    Routes the action to correct function.
    """
    if action == 'add':
        if not (name and contact and mail_id):
            return {'error': 'Missing name, contact or mail id for add'}, 400
        return add_user(name, contact, mail_id)

    elif action == 'update':
        if not (name and contact and mail_id):
            return {'error': 'Missing name, contact or mail id for update'}, 400
        return update_user(name, contact, mail_id)

    elif action == 'delete':
        if not (name or contact or mail_id):
            return {'error': 'At least one identifier (name/contact/mail id) required for delete'}
        return delete_user(name, contact, mail_id)

    else:
        return {'error': 'Invalid action. Use add, update or delete'}
