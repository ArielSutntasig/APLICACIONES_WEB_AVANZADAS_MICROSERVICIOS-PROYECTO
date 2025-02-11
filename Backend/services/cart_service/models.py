from . import db
from datetime import timedelta

class Carrito(db.Model):
    __bind_key__ = 'cart'
    __tablename__ = 'Carrito'
    Id = db.Column(db.Integer, primary_key=True)
    UsuarioId = db.Column(db.Integer, nullable=False)  # Referencia lógica
    ProductoId = db.Column(db.Integer, nullable=False) # Referencia lógica
    Cantidad = db.Column(db.Integer, nullable=False)
    PrecioUnitario = db.Column(db.Float, nullable=False)
    Estado = db.Column(db.String(50), nullable=False, default='Pendiente')
    Fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
