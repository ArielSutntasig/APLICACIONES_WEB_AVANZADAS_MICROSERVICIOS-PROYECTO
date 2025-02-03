from flask import request, jsonify
from . import order_bp
from app import db  # Para evitar ciclos de importación
from .models import Orden, DetalleOrden
from services.product_service.models import Producto  # Para actualizar el stock

@order_bp.route('/confirmar-compra', methods=['POST'])
def confirmar_compra():
    try:
        data = request.json
        nueva_orden = Orden(
            usuario_id=data['UsuarioId'],
            subtotal=data['Subtotal'],
            iva=data['IVA'],
            envio=data['Envio'],
            total=data['Total']
        )
        db.session.add(nueva_orden)
        db.session.flush()  # Permite obtener el ID de la orden

        for prod in data['productos']:
            detalle = DetalleOrden(
                orden_id=nueva_orden.Id,
                producto_id=prod['Id'],
                cantidad=prod['Cantidad'],
                precio_unitario=prod['PrecioUnitario']
            )
            db.session.add(detalle)
            producto_db = Producto.query.get(prod['Id'])
            if producto_db:
                if producto_db.stock >= prod['Cantidad']:
                    producto_db.stock -= prod['Cantidad']
                else:
                    raise Exception(f"Stock insuficiente para {producto_db.Nombre}")
        db.session.commit()
        return jsonify({"message": "Compra realizada con éxito", "orden_id": nueva_orden.Id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@order_bp.route('/ordenes/<int:UsuarioId>', methods=['GET'])
def obtener_ordenes(UsuarioId):
    try:
        ordenes = Orden.query.filter_by(UsuarioId=UsuarioId).order_by(Orden.Fecha.desc()).all()
        return jsonify([{
            "id": orden.Id,
            "fecha": orden.Fecha.isoformat(),
            "total": float(orden.Total),
            "estado": orden.Estado
        } for orden in ordenes]), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener órdenes: {e}"}), 500

@order_bp.route('/orden/<int:OrdenId>', methods=['GET'])
def obtener_detalle_orden(OrdenId):
    try:
        detalles = DetalleOrden.query.filter_by(OrdenId=OrdenId).all()
        return jsonify([{
            "producto_id": detalle.ProductoId,
            "cantidad": detalle.Cantidad,
            "precio_unitario": float(detalle.PrecioUnitario)
        } for detalle in detalles]), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener detalles de la orden: {e}"}), 500
