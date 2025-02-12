# API_Gateway/config.py

class Config:
    # URLs base de los microservicios
    USER_SERVICE_URL = "http://localhost:5001"
    PRODUCT_SERVICE_URL = "http://localhost:5002"   # Asumiendo que este servicio corre en el puerto 5002
    ORDER_SERVICE_URL = "http://localhost:5003"     # Asumiendo que este servicio corre en el puerto 5003
    CART_SERVICE_URL = "http://localhost:5004"      # Asumiendo que este servicio corre en el puerto 5004
    CHAT_SERVICE_URL = "http://localhost:5005"
