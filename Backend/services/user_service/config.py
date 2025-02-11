import os
from datetime import timedelta

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://administrador:admin1234#@apps-server.database.windows.net:1433/TechShop_UserService?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=no&Encrypt=yes"
    SQLALCHEMY_BINDS = {
        'user': "mssql+pyodbc://administrador:admin1234#@apps-server.database.windows.net:1433/TechShop_UserService?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=no&Encrypt=yes"
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'tu-clave-secreta-muy-segura')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)