from flask import Blueprint, request, jsonify
from app import db
from app.models.nutrientes import Nutrientes
from app.utils.jwt_utils import token_required

nutrientes_bp = Blueprint('nutrientes', __name__)

@nutrientes_bp.route('/', methods=['GET'])
@token_required
def get_nutrientes():
    nutrientes = Nutrientes.query.all()
    return jsonify([{
        "id_nutriente": n.id_nutriente,
        "nombre": n.nombre,
        "unidad": n.unidad
    } for n in nutrientes])

@nutrientes_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_nutriente(id):
    nutriente = Nutrientes.query.get_or_404(id)
    return jsonify({
        "id_nutriente": nutriente.id_nutriente,
        "nombre": nutriente.nombre,
        "unidad": nutriente.unidad
    })

@nutrientes_bp.route('/', methods=['POST'])
@token_required
def create_nutriente():
    data = request.get_json()
    new_nutriente = Nutrientes(
        nombre=data.get('nombre'),
        unidad=data.get('unidad')
    )
    db.session.add(new_nutriente)
    db.session.commit()
    return jsonify({"message": "Nutriente created", "id": new_nutriente.id_nutriente}), 201

@nutrientes_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_nutriente(id):
    nutriente = Nutrientes.query.get_or_404(id)
    data = request.get_json()
    nutriente.nombre = data.get('nombre', nutriente.nombre)
    nutriente.unidad = data.get('unidad', nutriente.unidad)
    db.session.commit()
    return jsonify({"message": "Nutriente updated"})

@nutrientes_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_nutriente(id):
    nutriente = Nutrientes.query.get_or_404(id)
    db.session.delete(nutriente)
    db.session.commit()
    return jsonify({"message": "Nutriente deleted"})