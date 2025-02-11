from flask import request
from flask_socketio import emit
import requests
from . import socketio

# Configuración del servicio de usuarios
USER_SERVICE_URL = "http://localhost:5001/api/user"
ASESOR_EMAIL = 'asesor.comercial@gmail.com'
usuarios_conectados = {}

def register_socket_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        print(f"Usuario conectado: {request.sid}")
        emit('connected', {'status': 'success'})

    @socketio.on('login')
    def handle_login(data):
        try:
            print(f"Intento de login con datos: {data}")
            usuario_id = data.get('usuario_id')
            email = data.get('email')
            
            if not usuario_id or not email:
                emit('error', {'error': 'Datos incompletos para el login.'})
                return

            # Verificar usuario mediante API
            response = requests.get(f"{USER_SERVICE_URL}/usuario/{usuario_id}")
            if response.status_code != 200:
                emit('error', {'error': 'Usuario no encontrado.'})
                return

            usuarios_conectados[str(usuario_id)] = {
                'id': usuario_id,
                'email': email,
                'sid': request.sid
            }
            
            print(f"Usuario {email} conectado con sid: {request.sid}")
            
            if email == ASESOR_EMAIL:
                print("Cargando mensajes pendientes para el asesor.")
                # Obtener mensajes pendientes mediante API
                response = requests.get(f"{USER_SERVICE_URL}/mensajes/pendientes/{usuario_id}")
                if response.status_code == 200:
                    mensajes_pendientes = response.json()
                    
                    print(f"Mensajes pendientes encontrados: {len(mensajes_pendientes)}")
                    
                    for mensaje in mensajes_pendientes:
                        emit('mensaje_nuevo', mensaje)
                    
                    # Marcar mensajes como leídos
                    requests.post(f"{USER_SERVICE_URL}/mensajes/marcar-leidos/{usuario_id}")

            emit('login_success', {
                'usuario_id': usuario_id,
                'email': email
            })

        except Exception as e:
            print(f"Error en login: {e}")
            emit('error', {'error': f'Error en el servidor: {str(e)}'})

    @socketio.on('enviar_mensaje')
    def handle_enviar_mensaje(data):
        try:
            emisor_id = data['emisor_id']
            receptor_id = data.get('receptor_id')
            contenido = data['contenido']

            # Crear mensaje mediante API
            response = requests.post(f"{USER_SERVICE_URL}/mensajes", json={
                'emisor_id': emisor_id,
                'receptor_id': receptor_id,
                'contenido': contenido
            })

            if response.status_code != 200:
                raise Exception("Error al crear el mensaje")

            mensaje_data = response.json()

            if str(receptor_id) in usuarios_conectados:
                emit('mensaje_nuevo', mensaje_data, room=usuarios_conectados[str(receptor_id)]['sid'])
            
            # Si el receptor es el asesor, actualizar notificaciones
            if str(receptor_id) in usuarios_conectados and usuarios_conectados[str(receptor_id)]['email'] == ASESOR_EMAIL:
                emit('actualizar_notificacion', {
                    'cliente_id': emisor_id,
                    'increment': True
                }, broadcast=True)

        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
            emit('error', {'error': str(e)})

    @socketio.on('disconnect')
    def handle_disconnect():
        try:
            for usuario_id, datos in list(usuarios_conectados.items()):
                if datos['sid'] == request.sid:
                    print(f"Usuario {datos['email']} desconectado")
                    del usuarios_conectados[usuario_id]
                    break
        except Exception as e:
            print(f"Error en disconnect: {e}")

    @socketio.on_error()
    def error_handler(e):
        print(f"Error en WebSocket: {e}")
        emit('error', {'error': 'Error interno del servidor'})

    return socketio