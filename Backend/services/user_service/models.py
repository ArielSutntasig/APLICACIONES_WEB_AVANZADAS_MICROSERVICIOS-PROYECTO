from . import db
from datetime import datetime

class Usuario(db.Model):
    __bind_key__ = 'user'
    __tablename__ = 'Usuarios'
    Id = db.Column(db.Integer, primary_key=True)
    NombreCompleto = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Contraseña = db.Column(db.String(255), nullable=False)
    FechaRegistro = db.Column(db.DateTime, default=datetime.utcnow)

    mensajes_recibidos = db.relationship('Mensaje', foreign_keys='Mensaje.ReceptorId', backref='receptor', lazy='dynamic')
    mensajes_enviados = db.relationship('Mensaje', foreign_keys='Mensaje.EmisorId', backref='emisor', lazy='dynamic')

class Mensaje(db.Model):
    __bind_key__ = 'user'
    __tablename__ = 'Mensajes'
    Id = db.Column(db.Integer, primary_key=True)
    EmisorId = db.Column(db.Integer, db.ForeignKey('Usuarios.Id'), nullable=False)
    ReceptorId = db.Column(db.Integer, db.ForeignKey('Usuarios.Id'), nullable=False)
    Contenido = db.Column(db.Text, nullable=False)
    Leido = db.Column(db.Boolean, default=False)
    Fecha = db.Column(db.DateTime, default=datetime.utcnow)