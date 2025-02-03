from app import db

class Producto(db.Model):
    __bind_key__ = 'product'
    __tablename__ = 'Productos'
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Precio = db.Column(db.Float, nullable=False)
    ImagenURL = db.Column(db.String(255), nullable=True)
    EnOferta = db.Column(db.Boolean, default=False)
    Stock = db.Column(db.Integer, default=0)
    FechaCreacion = db.Column(db.DateTime, default=db.func.current_timestamp())
