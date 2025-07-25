from flask import Blueprint, request, jsonify
from app import db
from app.models.municipio import Municipio
from app.utils.jwt_utils import token_required

municipio_bp = Blueprint('municipio', __name__)

@municipio_bp.route('/', methods=['GET'])
@token_required
def get_municipios():
    municipios = Municipio.query.all()
    return jsonify([{
        "id_municipio": m.id_municipio,
        "nombre_municipio": m.nombre_municipio,
        "id_departamento": m.id_departamento
    } for m in municipios])

@municipio_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_municipio(id):
    municipio = Municipio.query.get_or_404(id)
    return jsonify({
        "id_municipio": municipio.id_municipio,
        "nombre_municipio": municipio.nombre_municipio,
        "id_departamento": municipio.id_departamento
    })

@municipio_bp.route('/', methods=['POST'])
@token_required
def create_municipio():
    data = request.get_json()
    new_municipio = Municipio(
        nombre_municipio=data.get('nombre_municipio'),
        id_departamento=data.get('id_departamento')
    )
    db.session.add(new_municipio)
    db.session.commit()
    return jsonify({"message": "Municipio created", "id": new_municipio.id_municipio}), 201

@municipio_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_municipio(id):
    municipio = Municipio.query.get_or_404(id)
    data = request.get_json()
    municipio.nombre_municipio = data.get('nombre_municipio', municipio.nombre_municipio)
    municipio.id_departamento = data.get('id_departamento', municipio.id_departamento)
    db.session.commit()
    return jsonify({"message": "Municipio updated"})

@municipio_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_municipio(id):
    municipio = Municipio.query.get_or_404(id)
    db.session.delete(municipio)
    db.session.commit()
    return jsonify({"message": "Municipio deleted"})