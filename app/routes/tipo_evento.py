from flask import Blueprint, request, jsonify
from app import db
from app.models.tipo_evento import TipoEvento
from app.utils.jwt_utils import token_required

tipo_evento_bp = Blueprint('tipo_evento', __name__)

@tipo_evento_bp.route('/', methods=['GET'])
@token_required
def get_tipos_evento():
    tipos = TipoEvento.query.all()
    return jsonify([{
        "id_tipo_evento": t.id_tipo_evento,
        "nombre_tipo": t.nombre_tipo
    } for t in tipos])

@tipo_evento_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_tipo_evento(id):
    tipo = TipoEvento.query.get_or_404(id)
    return jsonify({
        "id_tipo_evento": tipo.id_tipo_evento,
        "nombre_tipo": tipo.nombre_tipo
    })

@tipo_evento_bp.route('/', methods=['POST'])
@token_required
def create_tipo_evento():
    data = request.get_json()
    new_tipo = TipoEvento(
        nombre_tipo=data.get('nombre_tipo')
    )
    db.session.add(new_tipo)
    db.session.commit()
    return jsonify({"message": "Tipo evento created", "id": new_tipo.id_tipo_evento}), 201

@tipo_evento_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_tipo_evento(id):
    tipo = TipoEvento.query.get_or_404(id)
    data = request.get_json()
    tipo.nombre_tipo = data.get('nombre_tipo', tipo.nombre_tipo)
    db.session.commit()
    return jsonify({"message": "Tipo evento updated"})

@tipo_evento_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_tipo_evento(id):
    tipo = TipoEvento.query.get_or_404(id)
    db.session.delete(tipo)
    db.session.commit()
    return jsonify({"message": "Tipo evento deleted"})