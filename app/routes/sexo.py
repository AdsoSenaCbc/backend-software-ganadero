from flask import Blueprint, request, jsonify
from app import db
from app.models.sexo import Sexo
from app.utils.jwt_utils import token_required

sexo_bp = Blueprint('sexo', __name__)

@sexo_bp.route('/', methods=['GET'])
@token_required
def get_sexos():
    sexos = Sexo.query.all()
    return jsonify([{
        "id_sexo": s.id_sexo,
        "nombre": s.nombre
    } for s in sexos])

@sexo_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_sexo(id):
    sexo = Sexo.query.get_or_404(id)
    return jsonify({
        "id_sexo": sexo.id_sexo,
        "nombre": sexo.nombre
    })

@sexo_bp.route('/', methods=['POST'])
@token_required
def create_sexo():
    data = request.get_json()
    new_sexo = Sexo(
        nombre=data.get('nombre')
    )
    db.session.add(new_sexo)
    db.session.commit()
    return jsonify({"message": "Sexo created", "id": new_sexo.id_sexo}), 201

@sexo_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_sexo(id):
    sexo = Sexo.query.get_or_404(id)
    data = request.get_json()
    sexo.nombre = data.get('nombre', sexo.nombre)
    db.session.commit()
    return jsonify({"message": "Sexo updated"})

@sexo_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_sexo(id):
    sexo = Sexo.query.get_or_404(id)
    db.session.delete(sexo)
    db.session.commit()
    return jsonify({"message": "Sexo deleted"})