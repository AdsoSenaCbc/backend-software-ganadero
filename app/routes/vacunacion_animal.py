from flask import Blueprint, request, jsonify
from app import db
from app.models.vacunacion_animal import VacunacionAnimal
from app.utils.jwt_utils import token_required

vacunacion_animal_bp = Blueprint('vacunacion_animal', __name__)

@vacunacion_animal_bp.route('/', methods=['GET'])
@vacunacion_animal_bp.route('/index', methods=['GET'])
@token_required
def index():
    vacunaciones = VacunacionAnimal.query.all()
    return jsonify([{
        "id_vacunacion": v.id_vacunacion,
        "id_animal": v.id_animal,
        "id_vacuna": v.id_vacuna,
        "id_lote": v.id_lote,
        "fecha_aplicacion": v.fecha_aplicacion.isoformat() if v.fecha_aplicacion else None,
        "dosis_aplicada": v.dosis_aplicada,
        "observaciones": v.observaciones
    } for v in vacunaciones])

@vacunacion_animal_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_vacunacion_animal(id):
    vacunacion = VacunacionAnimal.query.get_or_404(id)
    return jsonify({
        "id_vacunacion": vacunacion.id_vacunacion,
        "id_animal": vacunacion.id_animal,
        "id_vacuna": vacunacion.id_vacuna,
        "id_lote": vacunacion.id_lote,
        "fecha_aplicacion": vacunacion.fecha_aplicacion.isoformat(),
        "dosis_aplicada": vacunacion.dosis_aplicada,
        "observaciones": vacunacion.observaciones
    })

@vacunacion_animal_bp.route('/', methods=['POST'])
@token_required
def create_vacunacion_animal():
    data = request.get_json()
    new_vacunacion = VacunacionAnimal(
        id_animal=data.get('id_animal'),
        id_vacuna=data.get('id_vacuna'),
        id_lote=data.get('id_lote'),
        dosis_aplicada=data.get('dosis_aplicada'),
        observaciones=data.get('observaciones')
    )
    db.session.add(new_vacunacion)
    db.session.commit()
    return jsonify({"message": "Vacunacion animal created", "id": new_vacunacion.id_vacunacion}), 201

@vacunacion_animal_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_vacunacion_animal(id):
    vacunacion = VacunacionAnimal.query.get_or_404(id)
    data = request.get_json()
    vacunacion.id_animal = data.get('id_animal', vacunacion.id_animal)
    vacunacion.id_vacuna = data.get('id_vacuna', vacunacion.id_vacuna)
    vacunacion.id_lote = data.get('id_lote', vacunacion.id_lote)
    vacunacion.dosis_aplicada = data.get('dosis_aplicada', vacunacion.dosis_aplicada)
    vacunacion.observaciones = data.get('observaciones', vacunacion.observaciones)
    db.session.commit()
    return jsonify({"message": "Vacunacion animal updated"})

@vacunacion_animal_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_vacunacion_animal(id):
    vacunacion = VacunacionAnimal.query.get_or_404(id)
    db.session.delete(vacunacion)
    db.session.commit()
    return jsonify({"message": "Vacunacion animal deleted"})