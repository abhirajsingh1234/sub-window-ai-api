from app.utils.Load_Save import load_data, save_data

def add_user(name, contact, mail_id):
    """
    Add a new user if name, contact, and mail_id are unique.
    """
    data = load_data()

    if any(entry['name'] == name or entry['contact'] == contact or entry['mail id'] == mail_id for entry in data):
        return {'error': 'Duplicate entry detected (name/contact/mail id already exists)'}

    data.append({'name': name, 'contact': contact, 'mail id': mail_id})
    save_data(data)
    return {'message': 'User added successfully', 'data': data}
