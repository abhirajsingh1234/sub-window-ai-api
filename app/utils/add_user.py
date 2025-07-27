# from app.utils.Load_Save import load_data, save_data

# def add_user(name, contact, mail_id):
#     """
#     Add a new user if name, contact, and mail_id are unique.
#     """
#     data = load_data()

#     if any(entry['name'] == name or entry['contact'] == contact or entry['mail id'] == mail_id for entry in data):
#         return {'error': 'Duplicate entry detected (name/contact/mail id already exists)'}

#     data.append({'name': name, 'contact': contact, 'mail id': mail_id})
#     save_data(data)
#     return {'message': 'User added successfully', 'data': data}



from app.utils.Load_Save import load_data, save_data

def add_user(name, contact, mail_id):
    """
    Add a new user if name, contact, and mail_id are unique (ignores None values).
    """
    data = load_data()

    contact = None if len(contact) == 0 else contact
    mail_id = None if len(mail_id) == 0 else mail_id

    for entry in data:
        if name == entry.get('name'):
            return {'error': 'Duplicate name detected'}
        if contact is not None and contact == entry.get('contact'):
            return {'error': 'Duplicate contact detected'}
        if mail_id is not None and mail_id == entry.get('mail id'):
            return {'error': 'Duplicate mail id detected'}

    data.append({'name': name, 'contact': contact, 'mail id': mail_id})
    save_data(data)
    return {'message': 'User added successfully', 'data': data}
