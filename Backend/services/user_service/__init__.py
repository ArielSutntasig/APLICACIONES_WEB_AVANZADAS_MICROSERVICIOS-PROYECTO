# user_service/__init__.py
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .config import Config

# Inicialización de extensiones
db = SQLAlchemy()
jwt = JWTManager()

# Definir el blueprint
user_bp = Blueprint('user', __name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar extensiones con la app
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Importar las rutas (que usarán el blueprint y db)
    from . import routes
    app.register_blueprint(user_bp, url_prefix="/api/user")
    
    return app
