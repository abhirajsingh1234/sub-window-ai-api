from app.utils.Load_Save import load_data, save_data

def delete_user(name=None, contact=None, mail_id=None):
    """
    Delete user by name, contact, or mail_id.
    Priority: name → mail_id → contact
    """
    data = load_data()

    def find_index(value):
        for i, entry in enumerate(data):
            if (
                entry.get('name') == value
                or entry.get('contact') == value
                or entry.get('mail_id') == value
            ):
                return i
        return -1

    index = -1
    if name:
        index = find_index(name)
    if index == -1 and mail_id:
        index = find_index(mail_id)
    if index == -1 and contact:
        index = find_index(contact)

    if index == -1:
        return {'error': 'User not found for deletion'}

    deleted = data.pop(index)
    save_data(data)
    return {'message': f"Deleted user: {deleted}", 'data': data}
