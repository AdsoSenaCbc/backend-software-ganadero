from flask import Blueprint, request, jsonify
from app import db
from app.models.historial_animal import HistorialAnimal
from app.utils.jwt_utils import token_required

historial_animal_bp = Blueprint('historial_animal', __name__)

@historial_animal_bp.route('/', methods=['GET'])
@token_required
def get_historiales_animal():
    historiales = HistorialAnimal.query.all()
    return jsonify([{
        "id_historial": h.id_historial,
        "id_animal": h.id_animal,
        "id_hacienda": h.id_hacienda,
        "fecha_ingreso": h.fecha_ingreso.isoformat(),
        "fecha_salida": h.fecha_salida.isoformat() if h.fecha_salida else None,
        "observaciones": h.observaciones
    } for h in historiales])

@historial_animal_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_historial_animal(id):
    historial = HistorialAnimal.query.get_or_404(id)
    return jsonify({
        "id_historial": historial.id_historial,
        "id_animal": historial.id_animal,
        "id_hacienda": historial.id_hacienda,
        "fecha_ingreso": historial.fecha_ingreso.isoformat(),
        "fecha_salida": historial.fecha_salida.isoformat() if historial.fecha_salida else None,
        "observaciones": historial.observaciones
    })

@historial_animal_bp.route('/', methods=['POST'])
@token_required
def create_historial_animal():
    data = request.get_json()
    new_historial = HistorialAnimal(
        id_animal=data.get('id_animal'),
        id_hacienda=data.get('id_hacienda'),
        fecha_salida=data.get('fecha_salida'),
        observaciones=data.get('observaciones')
    )
    db.session.add(new_historial)
    db.session.commit()
    return jsonify({"message": "Historial animal created", "id": new_historial.id_historial}), 201

@historial_animal_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_historial_animal(id):
    historial = HistorialAnimal.query.get_or_404(id)
    data = request.get_json()
    historial.id_animal = data.get('id_animal', historial.id_animal)
    historial.id_hacienda = data.get('id_hacienda', historial.id_hacienda)
    historial.fecha_salida = data.get('fecha_salida', historial.fecha_salida)
    historial.observaciones = data.get('observaciones', historial.observaciones)
    db.session.commit()
    return jsonify({"message": "Historial animal updated"})

@historial_animal_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_historial_animal(id):
    historial = HistorialAnimal.query.get_or_404(id)
    db.session.delete(historial)
    db.session.commit()
    return jsonify({"message": "Historial animal deleted"})