# product_service/models.py
from . import db
from datetime import datetime

class Producto(db.Model):
    # Si utilizas múltiples bases de datos, puedes especificar el bind key. 
    # Asegúrate de configurar SQLALCHEMY_BINDS en la configuración de la app si es necesario. 
    __bind_key__ = 'product'
    __tablename__ = 'Productos'
    
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Precio = db.Column(db.Float, nullable=False)
    ImagenURL = db.Column(db.String(255), nullable=True)
    EnOferta = db.Column(db.Boolean, default=False)
    Stock = db.Column(db.Integer, default=0)
    # Usamos datetime.utcnow para obtener la hora actual
    FechaCreacion = db.Column(db.DateTime, default=datetime.utcnow)
