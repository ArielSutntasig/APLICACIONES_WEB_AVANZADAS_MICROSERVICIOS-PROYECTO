# order_service/__init__.py
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .config import Config

# Inicialización de la extensión SQLAlchemy
db = SQLAlchemy()
jwt = JWTManager()

# Definir el blueprint
order_bp = Blueprint('order', __name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Si no cuentas con config.py, puedes configurar directamente aquí

    # Inicializar extensiones con la app
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Importar las rutas y registrar el blueprint
    from . import routes
    
    app.register_blueprint(order_bp, url_prefix="/api/order")
    
    return app
