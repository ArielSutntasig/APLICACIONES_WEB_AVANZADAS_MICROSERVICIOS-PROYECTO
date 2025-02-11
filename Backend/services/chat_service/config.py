import os

class Config:
    # Socket.IO configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'tu-clave-secreta-muy-segura')