import os
from datetime import timedelta

class Config:
    # Configuración de la base de datos para el servicio de productos
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://sa:Politecnica1@localhost/TechShop_ProductService?driver=ODBC+Driver+17+for+SQL+Server"
    SQLALCHEMY_BINDS = {
        'product': "mssql+pyodbc://sa:Politecnica1@localhost/TechShop_ProductService?driver=ODBC+Driver+17+for+SQL+Server"
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    # Configuración de JWT (se incluye para mantener la similitud con el User Service)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'tu-clave-secreta-muy-segura')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
