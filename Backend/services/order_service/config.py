import os
from datetime import timedelta

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://sa:Politecnica1@localhost/TechShop_OrderService?driver=ODBC+Driver+17+for+SQL+Server"
    SQLALCHEMY_BINDS = {
        'order': "mssql+pyodbc://sa:Politecnica1@localhost/TechShop_OrderService?driver=ODBC+Driver+17+for+SQL+Server"
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    
    # Configuración de JWT (se incluye para mantener la similitud con el User Service)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'tu-clave-secreta-muy-segura')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)