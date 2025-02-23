# product_service/routes.py
from flask import request, jsonify
from . import product_bp, db
from .models import Producto

@product_bp.route('/productos', methods=['POST'])
def agregar_producto():
    data = request.json
    producto = Producto(
        Nombre=data.get('nombre'),
        Precio=data.get('precio'),
        ImagenURL=data.get('imagen_url'),
        EnOferta=data.get('en_oferta', False),
        Stock=data.get('stock')
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

@product_bp.route('/stock/<int:producto_id>', methods=['GET'])
def obtener_stock(producto_id):
    try:
        producto = Producto.query.get(producto_id)
        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404
        return jsonify({
            "id": producto.Id,
            "nombre": producto.Nombre,
            "stock": producto.Stock
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@product_bp.route('/actualizar-stock/<int:producto_id>', methods=['PUT'])
def actualizar_stock(producto_id):
    try:
        data = request.json
        cantidad = data.get('cantidad')
        
        producto = Producto.query.get(producto_id)
        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404
            
        if producto.Stock < cantidad:
            return jsonify({"error": "Stock insuficiente"}), 400
            
        producto.Stock -= cantidad
        db.session.commit()
        
        return jsonify({
            "message": "Stock actualizado correctamente",
            "nuevo_stock": producto.Stock
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500