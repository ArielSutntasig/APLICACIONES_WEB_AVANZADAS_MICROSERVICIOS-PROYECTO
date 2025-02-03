from flask import request
from flask_socketio import emit
from services.user_service.models import Usuario, Mensaje
from app import db
from datetime import datetime

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

            usuario = Usuario.query.get(usuario_id)
            if not usuario:
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
                mensajes_pendientes = Mensaje.query.filter_by(
                    ReceptorId=usuario_id,  # Cambio a mayúscula
                    Leido=False  # Cambio a mayúscula
                ).order_by(Mensaje.Fecha.asc()).all()  # Cambio a mayúscula
                
                print(f"Mensajes pendientes encontrados: {len(mensajes_pendientes)}")
                
                for mensaje in mensajes_pendientes:
                    emisor = Usuario.query.get(mensaje.EmisorId)
                    mensaje_data = {
                        'id': mensaje.Id,
                        'emisor_id': mensaje.EmisorId,
                        'emisor_nombre': emisor.NombreCompleto if emisor else 'Desconocido',
                        'contenido': mensaje.Contenido,
                        'fecha': mensaje.Fecha.isoformat()
                    }
                    print(f"Enviando mensaje pendiente: {mensaje_data}")
                    emit('mensaje_nuevo', mensaje_data)
                    mensaje.Leido = True
                
                db.session.commit()

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

            mensaje = Mensaje(
                EmisorId=emisor_id,
                ReceptorId=receptor_id,
                Contenido=contenido,
                Leido=False,
                Fecha=datetime.utcnow()
            )
            
            db.session.add(mensaje)
            db.session.commit()

            mensaje_data = {
                "id": mensaje.Id,
                "emisor_id": mensaje.EmisorId,
                "receptor_id": mensaje.ReceptorId,
                "contenido": mensaje.Contenido,
                "fecha": mensaje.Fecha.isoformat(),
                "leido": mensaje.Leido
            }

            if str(receptor_id) in usuarios_conectados:
                emit('mensaje_nuevo', mensaje_data, room=usuarios_conectados[str(receptor_id)]['sid'])
            
            # Si el receptor es el asesor, actualizar notificaciones
            asesor = Usuario.query.filter_by(Email=ASESOR_EMAIL).first()  # Cambio a mayúscula
            if asesor and receptor_id == asesor.Id:  # Cambio a mayúscula
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