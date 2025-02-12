import os
from datetime import timedelta
from urllib.parse import quote_plus

class Config:
    # Database configuration
    connection_string = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=tcp:apps-server.database.windows.net,1433;"
        "Database=TechShop_CartService;"
        "Uid=administrador;"
        "Pwd=admin1234#;"  # Reemplaza esto con tu contraseña
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
    SQLALCHEMY_BINDS = {
        'cart': f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    
    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'tu-clave-secreta-muy-segura')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)