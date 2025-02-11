from flask import Flask, Blueprint
from flask_socketio import SocketIO
from flask_cors import CORS
from .config import Config

# Initialize SocketIO
socketio = SocketIO()
chat_bp = Blueprint('chat', __name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    
    # Register blueprint
    from . import chat_routes
    app.register_blueprint(chat_bp, url_prefix="/api/chat")
    
    # Initialize SocketIO
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Register socket events
    chat_routes.register_socket_events(socketio)
    
    return app