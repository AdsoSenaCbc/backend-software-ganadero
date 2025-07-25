from flask import Blueprint, request, jsonify
from app import db
from app.models.nacimiento import Nacimiento
from app.utils.jwt_utils import token_required

nacimiento_bp = Blueprint('nacimiento', __name__)

@nacimiento_bp.route('/', methods=['GET'])
@token_required
def get_nacimientos():
    nacimientos = Nacimiento.query.all()
    return jsonify([{
        "id_nacimiento": n.id_nacimiento,
        "id_cria": n.id_cria,
        "id_madre": n.id_madre,
        "id_padre": n.id_padre,
        "fecha_nacimiento": n.fecha_nacimiento.isoformat(),
        "peso_nacimiento": float(n.peso_nacimiento),
        "tipo_parto": n.tipo_parto,
        "complicaciones": n.complicaciones,
        "observaciones": n.observaciones
    } for n in nacimientos])

@nacimiento_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_nacimiento(id):
    nacimiento = Nacimiento.query.get_or_404(id)
    return jsonify({
        "id_nacimiento": nacimiento.id_nacimiento,
        "id_cria": nacimiento.id_cria,
        "id_madre": nacimiento.id_madre,
        "id_padre": nacimiento.id_padre,
        "fecha_nacimiento": nacimiento.fecha_nacimiento.isoformat(),
        "peso_nacimiento": float(nacimiento.peso_nacimiento),
        "tipo_parto": nacimiento.tipo_parto,
        "complicaciones": nacimiento.complicaciones,
        "observaciones": nacimiento.observaciones
    })

@nacimiento_bp.route('/', methods=['POST'])
@token_required
def create_nacimiento():
    data = request.get_json()
    new_nacimiento = Nacimiento(
        id_cria=data.get('id_cria'),
        id_madre=data.get('id_madre'),
        id_padre=data.get('id_padre'),
        peso_nacimiento=data.get('peso_nacimiento'),
        tipo_parto=data.get('tipo_parto'),
        complicaciones=data.get('complicaciones'),
        observaciones=data.get('observaciones')
    )
    db.session.add(new_nacimiento)
    db.session.commit()
    return jsonify({"message": "Nacimiento created", "id": new_nacimiento.id_nacimiento}), 201

@nacimiento_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_nacimiento(id):
    nacimiento = Nacimiento.query.get_or_404(id)
    data = request.get_json()
    nacimiento.id_cria = data.get('id_cria', nacimiento.id_cria)
    nacimiento.id_madre = data.get('id_madre', nacimiento.id_madre)
    nacimiento.id_padre = data.get('id_padre', nacimiento.id_padre)
    nacimiento.peso_nacimiento = data.get('peso_nacimiento', nacimiento.peso_nacimiento)
    nacimiento.tipo_parto = data.get('tipo_parto', nacimiento.tipo_parto)
    nacimiento.complicaciones = data.get('complicaciones', nacimiento.complicaciones)
    nacimiento.observaciones = data.get('observaciones', nacimiento.observaciones)
    db.session.commit()
    return jsonify({"message": "Nacimiento updated"})

@nacimiento_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_nacimiento(id):
    nacimiento = Nacimiento.query.get_or_404(id)
    db.session.delete(nacimiento)
    db.session.commit()
    return jsonify({"message": "Nacimiento deleted"})