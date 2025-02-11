# user_service/routes.py
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from . import db, user_bp
from .models import Usuario, Mensaje

ASESOR_EMAIL = 'asesor.comercial@gmail.com'

@user_bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.json
    nombre = data.get('nombre_completo')
    email = data.get('email')
    contraseña = data.get('contraseña')
    if not nombre or not email or not contraseña:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400
    contraseña_hash = generate_password_hash(contraseña)
    nuevo_usuario = Usuario(NombreCompleto=nombre, Email=email, Contraseña=contraseña_hash)
    try:
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({"message": "Usuario creado exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"No se pudo crear el usuario: {e}"}), 500

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    try:
        usuario = Usuario.query.filter_by(Email=email).first()
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404
        if not check_password_hash(usuario.Contraseña, password):
            return jsonify({"error": "Contraseña incorrecta"}), 401

        # Asegurarse de que el ID sea un string al crear el token
        access_token = create_access_token(identity=str(usuario.Id))
        refresh_token = create_refresh_token(identity=str(usuario.Id))

        return jsonify({
            "message": "Inicio de sesión exitoso",
            "nombre_completo": usuario.NombreCompleto,
            "usuario_id": usuario.Id,
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {e}"}), 500

@user_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    return jsonify({"access_token": access_token}), 200

@user_bp.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.json
        email = data.get('email')
        new_password = data.get('new_password')

        print(f"1. Iniciando actualización de contraseña para: {email}")

        # Crear una única sesión para toda la operación
        with db.session.begin():
            # Actualizar directamente usando SQL
            result = db.session.execute(
                db.text("""
                    UPDATE Usuarios 
                    SET Contraseña = :nuevo_hash 
                    WHERE Email = :email
                """),
                {
                    'nuevo_hash': generate_password_hash(new_password),
                    'email': email
                }
            )
            
            # Verificar si se actualizó alguna fila
            if result.rowcount == 0:
                print("No se encontró el usuario para actualizar")
                return jsonify({"error": "Usuario no encontrado"}), 404
            
            print(f"2. Filas actualizadas: {result.rowcount}")
            
        return jsonify({"message": "Contraseña actualizada exitosamente"}), 200

    except Exception as e:
        print(f"Error en la actualización: {str(e)}")
        return jsonify({"error": f"Error al actualizar la contraseña: {str(e)}"}), 500

@user_bp.route('/usuario/<int:usuario_id>', methods=['GET'])
@jwt_required()
def obtener_nombre_usuario(usuario_id):
    try:
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify({"nombre_completo": usuario.NombreCompleto}), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener el nombre del usuario: {e}"}), 500

@user_bp.route('/obtener-asesor', methods=['GET'])
@jwt_required()
def obtener_asesor():
    try:
        asesor = Usuario.query.filter_by(Email=ASESOR_EMAIL).first()
        if not asesor:
            return jsonify({"error": "Asesor no encontrado"}), 404
        return jsonify({"asesor_id": asesor.Id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/obtener-chats-activos')
@jwt_required()
def obtener_chats_activos():
    try:
        asesor = Usuario.query.filter_by(Email=ASESOR_EMAIL).first()
        if not asesor:
            return jsonify({"error": "Asesor no encontrado"}), 404

        # Obtener usuarios con conteo de mensajes no leídos
        usuarios = db.session.query(
            Usuario.Id,
            Usuario.NombreCompleto,
            db.func.count(Mensaje.Id).label('mensajes_no_leidos')
        ).outerjoin(
            Mensaje,
            db.and_(
                Mensaje.EmisorId == Usuario.Id,
                Mensaje.ReceptorId == asesor.Id,
                Mensaje.Leido == False
            )
        ).filter(
            Usuario.Email != ASESOR_EMAIL
        ).group_by(
            Usuario.Id,
            Usuario.NombreCompleto
        ).all()

        result = [{
            "usuario_id": usuario[0],
            "nombre": usuario[1],
            "mensajes_no_leidos": usuario[2]
        } for usuario in usuarios]

        return jsonify(result)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@user_bp.route('/mensajes/<int:usuario_id>', methods=['GET'])
@jwt_required()
def obtener_mensajes(usuario_id):
    try:
        # Obtener el asesor
        asesor = Usuario.query.filter_by(Email=ASESOR_EMAIL).first()
        if not asesor:
            return jsonify({"error": "Asesor no encontrado"}), 404

        # Obtener mensajes entre el usuario y el asesor
        mensajes = Mensaje.query.filter(
            db.or_(
                db.and_(Mensaje.EmisorId == usuario_id, Mensaje.ReceptorId == asesor.Id),
                db.and_(Mensaje.EmisorId == asesor.Id, Mensaje.ReceptorId == usuario_id)
            )
        ).order_by(Mensaje.Fecha).all()

        return jsonify([{
            "id": mensaje.Id,
            "emisor_id": mensaje.EmisorId,
            "receptor_id": mensaje.ReceptorId,
            "contenido": mensaje.Contenido,
            "fecha": mensaje.Fecha.isoformat()
        } for mensaje in mensajes]), 200
    except Exception as e:
        print(f"Error al obtener mensajes: {str(e)}")
        return jsonify({"error": str(e)}), 500

@user_bp.route('/marcar-mensajes-leidos/<int:emisor_id>', methods=['POST'])
@jwt_required()
def marcar_mensajes_leidos(emisor_id):
    try:
        asesor = Usuario.query.filter_by(Email=ASESOR_EMAIL).first()
        if not asesor:
            return jsonify({"error": "Asesor no encontrado"}), 404

        # Marcar como leídos los mensajes del emisor al asesor
        Mensaje.query.filter_by(
            EmisorId=emisor_id,
            ReceptorId=asesor.Id,
            Leido=False
        ).update({"Leido": True})
        
        db.session.commit()
        return jsonify({"message": "Mensajes marcados como leídos"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@user_bp.route('/mensajes/pendientes/<int:usuario_id>', methods=['GET'])
def obtener_mensajes_pendientes(usuario_id):
    try:
        mensajes = Mensaje.query.filter_by(
            ReceptorId=usuario_id,
            Leido=False
        ).order_by(Mensaje.Fecha.asc()).all()
        
        return jsonify([{
            'id': mensaje.Id,
            'emisor_id': mensaje.EmisorId,
            'emisor_nombre': Usuario.query.get(mensaje.EmisorId).NombreCompleto,
            'contenido': mensaje.Contenido,
            'fecha': mensaje.Fecha.isoformat()
        } for mensaje in mensajes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/mensajes', methods=['POST'])
def crear_mensaje():
    try:
        data = request.json
        mensaje = Mensaje(
            EmisorId=data['emisor_id'],
            ReceptorId=data['receptor_id'],
            Contenido=data['contenido'],
            Leido=False
        )
        db.session.add(mensaje)
        db.session.commit()
        
        return jsonify({
            'id': mensaje.Id,
            'emisor_id': mensaje.EmisorId,
            'receptor_id': mensaje.ReceptorId,
            'contenido': mensaje.Contenido,
            'fecha': mensaje.Fecha.isoformat(),
            'leido': mensaje.Leido
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/mensajes/marcar-leidos/<int:usuario_id>', methods=['POST'])
def marcar_todos_mensajes_leidos(usuario_id):
    try:
        Mensaje.query.filter_by(
            ReceptorId=usuario_id,
            Leido=False
        ).update({'Leido': True})
        db.session.commit()
        return jsonify({'message': 'Mensajes marcados como leídos'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500