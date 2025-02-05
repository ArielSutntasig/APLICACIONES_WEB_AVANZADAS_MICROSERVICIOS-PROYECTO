import os
from datetime import timedelta

class Config:
    # Configuración existente de bases de datos
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://sa:Politecnica1@localhost/TechShop_UserService?driver=ODBC+Driver+17+for+SQL+Server"
    
    SQLALCHEMY_BINDS = {
        'product': "mssql+pyodbc://sa:Politecnica1@localhost/TechShop_ProductService?driver=ODBC+Driver+17+for+SQL+Server",
        'order': "mssql+pyodbc://sa:Politecnica1@localhost/TechShop_OrderService?driver=ODBC+Driver+17+for+SQL+Server",
        'cart': "mssql+pyodbc://sa:Politecnica1@localhost/TechShop_CartService?driver=ODBC+Driver+17+for+SQL+Server"
    }
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    # Configuración JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'tu-clave-secreta-muy-segura')  # Cambia esto en producción
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)