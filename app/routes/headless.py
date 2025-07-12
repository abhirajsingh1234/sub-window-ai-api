from flask import request, jsonify,Blueprint
import os

headless_bp = Blueprint('headless', __name__)

def update_env_variable(key, new_value, env_path=".env"):
    lines = []
    found_key = False

    if os.path.exists(env_path):
        with open(env_path, "r") as file:
            for line in file:
                key_part = line.split('=', 1)[0].strip()
                if key_part == key:
                    lines.append(f"{key}={new_value}\n")
                    found_key = True
                else:
                    lines.append(line)
    else:
        raise FileNotFoundError(f"{env_path} does not exist!")

    if not found_key:
        print(f"Key {key} not found, no update done.")

    with open(env_path, "w") as file:
        file.writelines(lines)

    os.environ[key] = str(new_value)


@headless_bp.route('/', methods=['POST'])
def update_headless():
    try:
        data = request.get_json(force=True)

        headless_str = str(data.get('headless', 'True')).lower()

        headless = headless_str in ['true', '1', 'yes']

        update_env_variable('HEADLESS', headless)

        return jsonify({"message": f"HEADLESS updated to {os.getenv('HEADLESS')}"}), 200

    except Exception as e:

        return jsonify({"error": str(e)}), 400