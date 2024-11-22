from flask import Flask

from app.extensions import socketio, cors
from app.routes import video_feed

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    
    # Enable CORS
    cors.init_app(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}})

    # Initialize extensions
    socketio.init_app(app, cors_allowed_origins="*")

    # Register blueprints
    app.register_blueprint(video_feed)

    return app