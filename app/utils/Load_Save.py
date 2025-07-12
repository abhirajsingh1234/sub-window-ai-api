import json
import os

DATA_FILE_PATH = r'C:\SubWindow\UnifiedContactMail.txt'

def load_data():
    """
    Load contact/mail data from file.
    Returns:
        list: List of user dictionaries.
    """
    if not os.path.exists(DATA_FILE_PATH):
        return []
    with open(DATA_FILE_PATH, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_data(data):
    """
    Save contact/mail data to file.
    Args:
        data (list): List of user dictionaries.
    Returns:
        bool: True if saved successfully, else False.
    """
    try:
        with open(DATA_FILE_PATH, 'w') as file:
            json.dump(data, file, indent=4)
        return True
    except:
        return False
