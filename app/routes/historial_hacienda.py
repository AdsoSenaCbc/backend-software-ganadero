from flask import Blueprint, request, jsonify
from app import db
from app.models.historial_hacienda import HistorialHacienda
from app.utils.jwt_utils import token_required

historial_hacienda_bp = Blueprint('historial_hacienda', __name__)

@historial_hacienda_bp.route('/', methods=['GET'])
@token_required
def get_historiales_hacienda():
    historiales = HistorialHacienda.query.all()
    return jsonify([{
        "id_historial": h.id_historial,
        "id_hacienda": h.id_hacienda,
        "fecha": h.fecha.isoformat(),
        "existencia_animales": float(h.existencia_animales),
        "area": float(h.area),
        "estado": h.estado,
        "observaciones": h.observaciones
    } for h in historiales])

@historial_hacienda_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_historial_hacienda(id):
    historial = HistorialHacienda.query.get_or_404(id)
    return jsonify({
        "id_historial": historial.id_historial,
        "id_hacienda": historial.id_hacienda,
        "fecha": historial.fecha.isoformat(),
        "existencia_animales": float(historial.existencia_animales),
        "area": float(historial.area),
        "estado": historial.estado,
        "observaciones": historial.observaciones
    })

@historial_hacienda_bp.route('/', methods=['POST'])
@token_required
def create_historial_hacienda():
    data = request.get_json()
    new_historial = HistorialHacienda(
        id_hacienda=data.get('id_hacienda'),
        existencia_animales=data.get('existencia_animales'),
        area=data.get('area'),
        estado=data.get('estado'),
        observaciones=data.get('observaciones')
    )
    db.session.add(new_historial)
    db.session.commit()
    return jsonify({"message": "Historial hacienda created", "id": new_historial.id_historial}), 201

@historial_hacienda_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_historial_hacienda(id):
    historial = HistorialHacienda.query.get_or_404(id)
    data = request.get_json()
    historial.id_hacienda = data.get('id_hacienda', historial.id_hacienda)
    historial.existencia_animales = data.get('existencia_animales', historial.existencia_animales)
    historial.area = data.get('area', historial.area)
    historial.estado = data.get('estado', historial.estado)
    historial.observaciones = data.get('observaciones', historial.observaciones)
    db.session.commit()
    return jsonify({"message": "Historial hacienda updated"})

@historial_hacienda_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_historial_hacienda(id):
    historial = HistorialHacienda.query.get_or_404(id)
    db.session.delete(historial)
    db.session.commit()
    return jsonify({"message": "Historial hacienda deleted"})