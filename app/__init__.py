from flask import Flask
from app.routes.agent import chat_bp
from app.routes.headless import headless_bp
from app.routes.AddDel import Add_Del_bp
from app.routes.FetchData import fetch_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(chat_bp,url_prefix = '/api/chat')
    app.register_blueprint(headless_bp, url_prefix = '/api/headless')
    app.register_blueprint(Add_Del_bp, url_prefix = '/api/add_del')
    app.register_blueprint(fetch_bp, url_prefix = '/api/fetch_details')

    return app
