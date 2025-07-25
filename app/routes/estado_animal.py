from flask import Blueprint, request, jsonify
from app import db
from app.models.estado_animal import EstadoAnimal
from app.utils.jwt_utils import token_required

estado_animal_bp = Blueprint('estado_animal', __name__)

@estado_animal_bp.route('/', methods=['GET'])
@token_required
def get_estados_animal():
    estados = EstadoAnimal.query.all()
    return jsonify([{
        "id_estado": e.id_estado,
        "nombre_estado": e.nombre_estado
    } for e in estados])

@estado_animal_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_estado_animal(id):
    estado = EstadoAnimal.query.get_or_404(id)
    return jsonify({
        "id_estado": estado.id_estado,
        "nombre_estado": estado.nombre_estado
    })

@estado_animal_bp.route('/', methods=['POST'])
@token_required
def create_estado_animal():
    data = request.get_json()
    new_estado = EstadoAnimal(
        nombre_estado=data.get('nombre_estado')
    )
    db.session.add(new_estado)
    db.session.commit()
    return jsonify({"message": "Estado animal created", "id": new_estado.id_estado}), 201

@estado_animal_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_estado_animal(id):
    estado = EstadoAnimal.query.get_or_404(id)
    data = request.get_json()
    estado.nombre_estado = data.get('nombre_estado', estado.nombre_estado)
    db.session.commit()
    return jsonify({"message": "Estado animal updated"})

@estado_animal_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_estado_animal(id):
    estado = EstadoAnimal.query.get_or_404(id)
    db.session.delete(estado)
    db.session.commit()
    return jsonify({"message": "Estado animal deleted"})