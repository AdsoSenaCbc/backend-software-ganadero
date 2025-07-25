from flask import Blueprint, request, jsonify
from app import db
from app.models.raza import Raza
from app.utils.jwt_utils import token_required

raza_bp = Blueprint('raza', __name__)

@raza_bp.route('/', methods=['GET'])
@token_required
def get_razas():
    razas = Raza.query.all()
    return jsonify([{
        "id_raza": r.id_raza,
        "nombre": r.nombre
    } for r in razas])

@raza_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_raza(id):
    raza = Raza.query.get_or_404(id)
    return jsonify({
        "id_raza": raza.id_raza,
        "nombre": raza.nombre
    })

@raza_bp.route('/', methods=['POST'])
@token_required
def create_raza():
    data = request.get_json()
    new_raza = Raza(
        nombre=data.get('nombre')
    )
    db.session.add(new_raza)
    db.session.commit()
    return jsonify({"message": "Raza created", "id": new_raza.id_raza}), 201

@raza_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_raza(id):
    raza = Raza.query.get_or_404(id)
    data = request.get_json()
    raza.nombre = data.get('nombre', raza.nombre)
    db.session.commit()
    return jsonify({"message": "Raza updated"})

@raza_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_raza(id):
    raza = Raza.query.get_or_404(id)
    db.session.delete(raza)
    db.session.commit()
    return jsonify({"message": "Raza deleted"})