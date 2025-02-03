from flask import request, jsonify
from . import cart_bp
from app import db
from services.product_service.models import Producto  # Se importa el modelo Producto de la ubicación correcta
from .models import Carrito  # Asegúrate de que el modelo Carrito esté definido e importado

@cart_bp.route('/carrito/<int:usuario_id>', methods=['GET'])
def obtener_carrito(usuario_id):
    try:
        print(f"Obteniendo carrito para usuario {usuario_id}")
        
        # Obtener items del carrito
        items = Carrito.query.filter_by(
            UsuarioId=usuario_id,
            Estado='Pendiente'
        ).all()

        if not items:
            return jsonify([]), 200

        # Obtener los IDs de productos
        producto_ids = [item.ProductoId for item in items]

        try:
            # Obtener productos usando el ORM
            productos = {
                producto.Id: {
                    'nombre': producto.Nombre,
                    'imagen_url': producto.ImagenURL,
                    'precio': float(producto.Precio)
                }
                for producto in Producto.query.filter(Producto.Id.in_(producto_ids)).all()
            }
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            productos = {}

        # Construir el carrito con la información completa
        carrito = []
        for item in items:
            producto_info = productos.get(item.ProductoId, {})
            carrito_item = {
                "id": item.Id,
                "producto_id": item.ProductoId,
                "producto": producto_info.get('nombre', 'Producto no encontrado'),
                "cantidad": item.Cantidad,
                "precio_unitario": float(item.PrecioUnitario),
                "imagen": producto_info.get('imagen_url', ''),
                "subtotal": float(item.PrecioUnitario * item.Cantidad)
            }
            carrito.append(carrito_item)

        print("Items en el carrito:", len(carrito))
        print("Primer item del carrito (ejemplo):", carrito[0] if carrito else "No hay items")
        return jsonify(carrito), 200

    except Exception as e:
        print("Error al obtener carrito:", str(e))
        return jsonify({"error": f"No se pudo obtener el carrito: {e}"}), 500

@cart_bp.route('/carrito', methods=['POST'])
def agregar_al_carrito():
    try:
        data = request.json
        print("Datos recibidos:", data)

        if not all(key in data for key in ['usuario_id', 'producto_id', 'cantidad', 'precio_unitario']):
            return jsonify({"error": "Faltan datos requeridos"}), 400

        carrito_existente = Carrito.query.filter_by(
            UsuarioId=data['usuario_id'],
            ProductoId=data['producto_id'],
            Estado='Pendiente'
        ).first()

        if carrito_existente:
            carrito_existente.Cantidad += data['cantidad']
            print(f"Actualizando cantidad en carrito existente: {carrito_existente.Cantidad}")
        else:
            carrito_item = Carrito(
                UsuarioId=data['usuario_id'],
                ProductoId=data['producto_id'],
                Cantidad=data['cantidad'],
                PrecioUnitario=data['precio_unitario'],
                Estado='Pendiente'
            )
            db.session.add(carrito_item)
            print("Agregando nuevo item al carrito")

        db.session.commit()
        return jsonify({"message": "Producto agregado al carrito"}), 201

    except Exception as e:
        print(f"Error en agregar_al_carrito: {str(e)}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@cart_bp.route('/carrito/actualizar', methods=['POST'])
def actualizar_carrito():
    try:
        data = request.json
        item = Carrito.query.get(data['item_id'])
        if not item:
            return jsonify({"error": "Item no encontrado"}), 404

        item.Cantidad = data['cantidad']
        db.session.commit()
        return jsonify({"message": "Cantidad actualizada"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@cart_bp.route('/carrito/eliminar/<int:item_id>', methods=['DELETE'])
def eliminar_del_carrito(item_id):
    try:
        item = Carrito.query.get(item_id)
        if not item:
            return jsonify({"error": "Item no encontrado"}), 404
            
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item eliminado"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500