from flask import Blueprint, request, jsonify
from app import db
from app.models.consulta_bromatologica import ConsultaBromatologica
from app.utils.jwt_utils import token_required

consulta_bromatologica_bp = Blueprint('consulta_bromatologica', __name__)

@consulta_bromatologica_bp.route('/', methods=['GET'])
@token_required
def index():
    consultas = ConsultaBromatologica.query.all()
    return jsonify([{
        "id_consulta": c.id_consulta,
        "fecha_consulta": c.fecha_consulta.isoformat(),
        "id_usuario": c.id_usuario
    } for c in consultas])

@consulta_bromatologica_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_consulta_bromatologica(id):
    consulta = ConsultaBromatologica.query.get_or_404(id)
    return jsonify({
        "id_consulta": consulta.id_consulta,
        "fecha_consulta": consulta.fecha_consulta.isoformat(),
        "id_usuario": consulta.id_usuario
    })

@consulta_bromatologica_bp.route('/', methods=['POST'])
@token_required
def create_consulta_bromatologica():
    data = request.get_json()
    new_consulta = ConsultaBromatologica(
        id_usuario=data.get('id_usuario')
    )
    db.session.add(new_consulta)
    db.session.commit()
    return jsonify({"message": "Consulta bromatologica created", "id": new_consulta.id_consulta}), 201

@consulta_bromatologica_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_consulta_bromatologica(id):
    consulta = ConsultaBromatologica.query.get_or_404(id)
    data = request.get_json()
    consulta.id_usuario = data.get('id_usuario', consulta.id_usuario)
    db.session.commit()
    return jsonify({"message": "Consulta bromatologica updated"})

@consulta_bromatologica_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_consulta_bromatologica(id):
    consulta = ConsultaBromatologica.query.get_or_404(id)
    db.session.delete(consulta)
    db.session.commit()
    return jsonify({"message": "Consulta bromatologica deleted"})