import json
import os

unified_path = r'C:\SubWindow\UnifiedContactMail.txt'

def unified_data():
    """
    Load all user entries from the unified data file.

    Returns:
        list: List of dictionaries with keys 'name', 'contact', and 'mail id'.
              Returns empty list if file is missing or invalid.
    """
    if not os.path.exists(unified_path):
        return []

    try:
        with open(unified_path, 'r') as f:
            return json.load(f)
    except Exception:
        return []


def mail_data():
    """
    Convert unified data into a {name: mail id} dictionary.

    Returns:
        dict: Mapping of name to email.
    """
    try:
        data = unified_data()
        return {entry['name']: entry['mail_id'] for entry in data if 'name' in entry and 'mail_id' in entry}
    except Exception:
        return {}

def contact_data():
    """
    Convert unified data into a {name: contact} dictionary.

    Returns:
        dict: Mapping of name to contact number.
    """
    try:
        data = unified_data()
        return {entry['name']: entry['contact'] for entry in data if 'name' in entry and 'contact' in entry}
    except Exception:
        return {}
