from flask import request, jsonify
import requests
from . import order_bp, db
from .models import Orden, DetalleOrden

# Configuración del servicio de productos
PRODUCT_SERVICE_URL = "http://localhost:5002/api/product"

@order_bp.route('/confirmar-compra', methods=['POST'])
def confirmar_compra():
   try:
       data = request.json
       nueva_orden = Orden(
           UsuarioId=data['usuario_id'],
           Subtotal=data['subtotal'],
           IVA=data['iva'],
           Envio=data['envio'],
           Total=data['total']
       )
       db.session.add(nueva_orden)
       db.session.flush()  # Permite obtener el ID de la orden

       for prod in data['productos']:
           detalle = DetalleOrden(
               OrdenId=nueva_orden.Id,
               ProductoId=prod['id'],
               Cantidad=prod['cantidad'],
               PrecioUnitario=prod['precio_unitario']
           )
           db.session.add(detalle)
           
           # Verifica stock mediante API
           response = requests.get(f"{PRODUCT_SERVICE_URL}/stock/{prod['id']}")
           if response.status_code == 200:
               producto_data = response.json()
               if producto_data['stock'] >= prod['cantidad']:
                   # Actualiza stock mediante API
                   requests.put(f"{PRODUCT_SERVICE_URL}/actualizar-stock/{prod['id']}", 
                              json={'cantidad': prod['cantidad']})
               else:
                   raise Exception(f"Stock insuficiente para el producto {prod['id']}")
           else:
               raise Exception("Error al verificar el stock del producto")

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