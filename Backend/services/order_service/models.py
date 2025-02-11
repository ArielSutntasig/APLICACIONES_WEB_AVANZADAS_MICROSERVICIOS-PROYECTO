from . import db
from datetime import timedelta

class Orden(db.Model):
    __bind_key__ = 'order'
    __tablename__ = 'Ordenes'
    Id = db.Column(db.Integer, primary_key=True)
    UsuarioId = db.Column(db.Integer, nullable=False)  # Referencia lógica
    Subtotal = db.Column(db.Numeric(10,2), nullable=False)
    IVA = db.Column(db.Numeric(10,2), nullable=False)
    Envio = db.Column(db.Numeric(10,2), nullable=False)
    Total = db.Column(db.Numeric(10,2), nullable=False)
    Estado = db.Column(db.String(50), default='Completada')
    Fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    detalles = db.relationship('DetalleOrden', backref='orden', lazy=True)

class DetalleOrden(db.Model):
    __bind_key__ = 'order'
    __tablename__ = 'DetallesOrden'
    Id = db.Column(db.Integer, primary_key=True)
    OrdenId = db.Column(db.Integer, db.ForeignKey('Ordenes.Id'), nullable=False)
    ProductoId = db.Column(db.Integer, nullable=False)  # Referencia lógica
    Cantidad = db.Column(db.Integer, nullable=False)
    PrecioUnitario = db.Column(db.Float, nullable=False)
