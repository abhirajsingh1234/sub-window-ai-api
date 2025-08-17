from flask import Flask, request
from flask_cors import CORS

from app.routes.agent import chat_bp
from app.routes.headless import headless_bp
from app.routes.AddDel import Add_Del_bp
from app.routes.FetchData import fetch_bp

def create_app():
    app = Flask(__name__)

    # ✅ Allow only React frontend
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}}, supports_credentials=True)

    # Register blueprints
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(headless_bp, url_prefix='/api/headless')
    app.register_blueprint(Add_Del_bp, url_prefix='/api/add_del')
    app.register_blueprint(fetch_bp, url_prefix='/api/fetch_details')

    # ✅ Make sure preflight OPTIONS requests don’t get blocked
    @app.before_request
    def handle_options():
        if request.method == "OPTIONS":
            return {}, 200

    return app
