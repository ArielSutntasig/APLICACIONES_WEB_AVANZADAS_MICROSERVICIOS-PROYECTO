import os
import logging
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import requests

# Configuración: Puedes ajustar estas URLs vía variables de entorno o en un archivo aparte.
class Config:
    USER_SERVICE_URL = os.environ.get("USER_SERVICE_URL", "http://localhost:5001")
    PRODUCT_SERVICE_URL = os.environ.get("PRODUCT_SERVICE_URL", "http://localhost:5002")
    ORDER_SERVICE_URL = os.environ.get("ORDER_SERVICE_URL", "http://localhost:5003")
    CART_SERVICE_URL = os.environ.get("CART_SERVICE_URL", "http://localhost:5004")
    CHAT_SERVICE_URL = os.environ.get("CHAT_SERVICE_URL", "http://localhost:5005")
    # Otras configuraciones, como SECRET_KEY, pueden agregarse aquí.

app = Flask(__name__)
app.config.from_object(Config)

# Habilitar CORS para todas las rutas API; en producción, especifica el origen permitido.
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = app.logger

# Función que reenvía la solicitud al microservicio destino
def proxy_request(target_url):
    # Si se trata de una solicitud preflight, responder de inmediato.
    if request.method == 'OPTIONS':
        logger.debug("Solicitud OPTIONS interceptada, respondiendo 200 sin reenviar.")
        return Response(status=200)
    
    # Copiar las cabeceras, exceptuando 'Host'
    headers = {key: value for key, value in request.headers if key.lower() != 'host'}
    logger.debug(f"Reenviando {request.method} a {target_url} con headers: {headers}")

    try:
        # Reenviar la solicitud según el método
        if request.method == "GET":
            resp = requests.get(target_url, params=request.args, headers=headers, timeout=10)
        elif request.method == "POST":
            # Se detecta si es JSON para reenviar el cuerpo adecuadamente.
            if request.is_json:
                resp = requests.post(target_url, json=request.get_json(), headers=headers, timeout=10)
            else:
                resp = requests.post(target_url, data=request.form, headers=headers, timeout=10)
        elif request.method == "PUT":
            if request.is_json:
                resp = requests.put(target_url, json=request.get_json(), headers=headers, timeout=10)
            else:
                resp = requests.put(target_url, data=request.form, headers=headers, timeout=10)
        elif request.method == "DELETE":
            resp = requests.delete(target_url, headers=headers, timeout=10)
        else:
            return jsonify({"error": "Método HTTP no soportado"}), 405
    except requests.exceptions.RequestException as e:
        logger.error(f"Error al conectar con {target_url}: {e}")
        return jsonify({"error": f"Error al conectar con el servicio: {e}"}), 502

    logger.debug(f"Respuesta recibida: {resp.status_code}, Content-Type: {resp.headers.get('Content-Type')}")
    # Excluir algunas cabeceras problemáticas
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers_response = [
        (name, value)
        for name, value in resp.raw.headers.items()
        if name.lower() not in excluded_headers
    ]
    return Response(resp.content, resp.status_code, headers_response)

# Rutas para reenviar las peticiones a los microservicios

@app.route("/api/user/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def user_service_proxy(path):
    target_url = f"{app.config['USER_SERVICE_URL']}/api/user/{path}"
    logger.debug(f"Proxy para USER: {target_url}")
    return proxy_request(target_url)

@app.route("/api/product/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def product_service_proxy(path):
    target_url = f"{app.config['PRODUCT_SERVICE_URL']}/api/product/{path}"
    logger.debug(f"Proxy para PRODUCT: {target_url}")
    return proxy_request(target_url)

@app.route("/api/order/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def order_service_proxy(path):
    target_url = f"{app.config['ORDER_SERVICE_URL']}/api/order/{path}"
    logger.debug(f"Proxy para ORDER: {target_url}")
    return proxy_request(target_url)

@app.route("/api/cart/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def cart_service_proxy(path):
    target_url = f"{app.config['CART_SERVICE_URL']}/api/cart/{path}"
    logger.debug(f"Proxy para CART: {target_url}")
    return proxy_request(target_url)

@app.route("/api/chat/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def chat_service_proxy(path):
    target_url = f"{app.config['CHAT_SERVICE_URL']}/api/chat/{path}"
    logger.debug(f"Proxy para CHAT: {target_url}")
    return proxy_request(target_url)

# Opcional: manejo global de errores para rutas no definidas o errores internos
@app.errorhandler(404)
def not_found(error):
    logger.error("Endpoint no encontrado: %s", request.path)
    return jsonify({"error": "Endpoint no encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error("Error interno: %s", error)
    return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    # Ejecuta el gateway en el puerto 5000
    app.run(debug=True, host="0.0.0.0", port=5000)
