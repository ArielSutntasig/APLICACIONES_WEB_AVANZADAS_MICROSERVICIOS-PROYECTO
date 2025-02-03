from flask import Flask
from config import Config
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS



# Creamos una única instancia de SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar extensiones
    db.init_app(app)
    socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

    # Habilitar CORS
    CORS(app)
    
    # Registrar los Blueprints de los servicios
    from services.user_service.routes import user_bp
    from services.product_service.routes import product_bp
    from services.order_service.routes import order_bp
    from services.cart_service.routes import cart_bp
    from services.chat_service.chat_routes import register_socket_events
    

    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(product_bp, url_prefix="/product")
    app.register_blueprint(order_bp, url_prefix="/order")
    app.register_blueprint(cart_bp, url_prefix="/cart")
    
    # Registrar eventos de chat
    register_socket_events(socketio)
    
    with app.app_context():
        # Crear todas las tablas en las bases de datos correspondientes.
        # SQLAlchemy utiliza la configuración y los binds para distribuir los modelos.
        db.create_all()
    
    return app, socketio

app, socketio = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
