from flask import request, jsonify
from . import product_bp
from app import db
from .models import Producto

@product_bp.route('/productos', methods=['POST'])
def agregar_producto():
    data = request.json
    producto = Producto(
        nombre=data.get('nombre'),
        precio=data.get('precio'),
        imagen_url=data.get('imagen_url'),
        en_oferta=data.get('en_oferta', False),
        stock=data.get('stock')
    )
    try:
        db.session.add(producto)
        db.session.commit()
        return jsonify({"message": "Producto agregado correctamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"No se pudo agregar el producto: {e}"}), 500

@product_bp.route('/productos', methods=['GET'])
def obtener_productos():
    try:
        productos = Producto.query.all()
        productos_list = []
        for producto in productos:
            try:
                productos_list.append({
                    "id": producto.Id,
                    "nombre": producto.Nombre,
                    "precio": float(producto.Precio),
                    "imagen_url": producto.ImagenURL or "/static/images/default-product.jpg",
                    "en_oferta": bool(producto.EnOferta),
                    "stock": int(producto.Stock),
                    "fecha_creacion": producto.FechaCreacion.isoformat() if producto.FechaCreacion else None
                })
            except Exception as e:
                print(f"Error procesando producto {producto.Id}: {str(e)}")
                continue
        return jsonify(productos_list), 200
    except Exception as e:
        print(f"Error al obtener productos: {str(e)}")
        return jsonify({"error": "Error al obtener productos"}), 500

@product_bp.route('/productos/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    try:
        data = request.json
        producto = Producto.query.get(producto_id)
        if producto:
            producto.Nombre = data.get('nombre', producto.Nombre)
            producto.Precio = data.get('precio', producto.Precio)
            producto.ImagenURL = data.get('imagen_url', producto.ImagenURL)
            producto.EnOferta = data.get('en_oferta', producto.EnOferta)
            producto.Stock = data.get('stock', producto.Stock)
            db.session.commit()
            return jsonify({"message": "Producto actualizado"}), 200
        return jsonify({"error": "Producto no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@product_bp.route('/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    try:
        producto = Producto.query.get(producto_id)
        if producto:
            db.session.delete(producto)
            db.session.commit()
            return jsonify({"message": "Producto eliminado"}), 200
        return jsonify({"error": "Producto no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@product_bp.route('/productos/<int:producto_id>', methods=['GET'])
def obtener_producto(producto_id):
    try:
        producto = Producto.query.get(producto_id)
        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404
        
        return jsonify({
            "id": producto.Id,
            "nombre": producto.Nombre,
            "precio": float(producto.Precio),
            "imagen_url": producto.ImagenURL,
            "en_oferta": producto.EnOferta,
            "stock": producto.Stock
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500