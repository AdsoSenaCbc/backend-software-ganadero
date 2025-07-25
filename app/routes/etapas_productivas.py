from flask import Blueprint, request, jsonify
from app import db
from app.models.etapas_productivas import EtapasProductivas
from app.utils.jwt_utils import token_required

etapas_productivas_bp = Blueprint('etapas_productivas', __name__)

@etapas_productivas_bp.route('/', methods=['GET'])
@token_required
def get_etapas_productivas():
    etapas = EtapasProductivas.query.all()
    return jsonify([{
        "id_etapa": e.id_etapa,
        "nombre": e.nombre,
        "descripcion": e.descripcion
    } for e in etapas])

@etapas_productivas_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_etapa_productiva(id):
    etapa = EtapasProductivas.query.get_or_404(id)
    return jsonify({
        "id_etapa": etapa.id_etapa,
        "nombre": etapa.nombre,
        "descripcion": etapa.descripcion
    })

@etapas_productivas_bp.route('/', methods=['POST'])
@token_required
def create_etapa_productiva():
    data = request.get_json()
    new_etapa = EtapasProductivas(
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion')
    )
    db.session.add(new_etapa)
    db.session.commit()
    return jsonify({"message": "Etapa productiva created", "id": new_etapa.id_etapa}), 201

@etapas_productivas_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_etapa_productiva(id):
    etapa = EtapasProductivas.query.get_or_404(id)
    data = request.get_json()
    etapa.nombre = data.get('nombre', etapa.nombre)
    etapa.descripcion = data.get('descripcion', etapa.descripcion)
    db.session.commit()
    return jsonify({"message": "Etapa productiva updated"})

@etapas_productivas_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_etapa_productiva(id):
    etapa = EtapasProductivas.query.get_or_404(id)
    db.session.delete(etapa)
    db.session.commit()
    return jsonify({"message": "Etapa productiva deleted"})