class Config:
    # La base de datos por defecto será para el User Service
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://sa:Politecnica1@localhost/TechShop_UserService?driver=ODBC+Driver+17+for+SQL+Server"
    
    # Definición de binds para los demás servicios
    SQLALCHEMY_BINDS = {
        'product': "mssql+pyodbc://sa:Politecnica1@localhost/TechShop_ProductService?driver=ODBC+Driver+17+for+SQL+Server",
        'order': "mssql+pyodbc://sa:Politecnica1@localhost/TechShop_OrderService?driver=ODBC+Driver+17+for+SQL+Server",
        'cart': "mssql+pyodbc://sa:Politecnica1@localhost/TechShop_CartService?driver=ODBC+Driver+17+for+SQL+Server"
    }
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
