# product_service/__init__.py
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .config import Config

# Inicializar las extensiones
db = SQLAlchemy()
jwt = JWTManager()

# Definir el blueprint para las rutas de productos
product_bp = Blueprint('product', __name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar las extensiones con la app
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Importar las rutas (esto registra las vistas en el blueprint)
    from . import routes
    
    # Registrar el blueprint en la aplicación
    app.register_blueprint(product_bp, url_prefix="/api/product")
    
    return app
