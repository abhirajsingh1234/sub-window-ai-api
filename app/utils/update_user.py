from app.utils.Load_Save import load_data, save_data

def update_user(name, contact, mail_id):
    """
    Update user data. Search by name, mail_id, or contact.
    """
    data = load_data()

    def find_index(value):
        for i, entry in enumerate(data):
            if entry['name'] == value or entry['contact'] == value or entry['mail id'] == value:
                return i
        return -1

    index = find_index(name)
    if index == -1 and mail_id:
        index = find_index(mail_id)
    if index == -1 and contact:
        index = find_index(contact)

    if index == -1:
        return {'error': 'User not found for update'}

    data[index] = {'name': name, 'contact': contact, 'mail id': mail_id}
    save_data(data)
    return {'message': 'User updated successfully', 'data': data}
