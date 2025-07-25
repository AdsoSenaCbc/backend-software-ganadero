from flask import Blueprint, request, jsonify
from app import db
from app.models.especie import Especie
from app.utils.jwt_utils import token_required

especie_bp = Blueprint('especie', __name__)

@especie_bp.route('/', methods=['GET'])
@token_required
def get_especies():
    especies = Especie.query.all()
    return jsonify([{
        "id_especie": e.id_especie,
        "nombre": e.nombre
    } for e in especies])

@especie_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_especie(id):
    especie = Especie.query.get_or_404(id)
    return jsonify({
        "id_especie": especie.id_especie,
        "nombre": especie.nombre
    })

@especie_bp.route('/', methods=['POST'])
@token_required
def create_especie():
    data = request.get_json()
    new_especie = Especie(
        nombre=data.get('nombre')
    )
    db.session.add(new_especie)
    db.session.commit()
    return jsonify({"message": "Especie created", "id": new_especie.id_especie}), 201

@especie_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_especie(id):
    especie = Especie.query.get_or_404(id)
    data = request.get_json()
    especie.nombre = data.get('nombre', especie.nombre)
    db.session.commit()
    return jsonify({"message": "Especie updated"})

@especie_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_especie(id):
    especie = Especie.query.get_or_404(id)
    db.session.delete(especie)
    db.session.commit()
    return jsonify({"message": "Especie deleted"})