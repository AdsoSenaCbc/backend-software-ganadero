from flask import Blueprint, request, jsonify
from app import db
from app.models.detalle_racion import DetalleRacion
from app.utils.jwt_utils import token_required

detalle_racion_bp = Blueprint('detalle_racion', __name__)

@detalle_racion_bp.route('/', methods=['GET'])
@token_required
def get_detalle_raciones():
    detalles = DetalleRacion.query.all()
    return jsonify([{
        "id_detalle": d.id_detalle,
        "id_racion": d.id_racion,
        "id_ingrediente": d.id_ingrediente,
        "cantidad_kg": float(d.cantidad_kg),
        "porcentaje_ms": float(d.porcentaje_ms)
    } for d in detalles])

@detalle_racion_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_detalle_racion(id):
    detalle = DetalleRacion.query.get_or_404(id)
    return jsonify({
        "id_detalle": detalle.id_detalle,
        "id_racion": detalle.id_racion,
        "id_ingrediente": detalle.id_ingrediente,
        "cantidad_kg": float(detalle.cantidad_kg),
        "porcentaje_ms": float(detalle.porcentaje_ms)
    })

@detalle_racion_bp.route('/', methods=['POST'])
@token_required
def create_detalle_racion():
    data = request.get_json()
    new_detalle = DetalleRacion(
        id_racion=data.get('id_racion'),
        id_ingrediente=data.get('id_ingrediente'),
        cantidad_kg=data.get('cantidad_kg'),
        porcentaje_ms=data.get('porcentaje_ms')
    )
    db.session.add(new_detalle)
    db.session.commit()
    return jsonify({"message": "Detalle racion created", "id": new_detalle.id_detalle}), 201

@detalle_racion_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_detalle_racion(id):
    detalle = DetalleRacion.query.get_or_404(id)
    data = request.get_json()
    detalle.id_racion = data.get('id_racion', detalle.id_racion)
    detalle.id_ingrediente = data.get('id_ingrediente', detalle.id_ingrediente)
    detalle.cantidad_kg = data.get('cantidad_kg', detalle.cantidad_kg)
    detalle.porcentaje_ms = data.get('porcentaje_ms', detalle.porcentaje_ms)
    db.session.commit()
    return jsonify({"message": "Detalle racion updated"})

@detalle_racion_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_detalle_racion(id):
    detalle = DetalleRacion.query.get_or_404(id)
    db.session.delete(detalle)
    db.session.commit()
    return jsonify({"message": "Detalle racion deleted"})