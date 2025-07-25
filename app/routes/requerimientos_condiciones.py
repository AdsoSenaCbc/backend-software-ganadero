from flask import Blueprint, request, jsonify
from app import db
from app.models.requerimientos_condiciones import RequerimientosCondiciones
from app.utils.jwt_utils import token_required

requerimientos_condiciones_bp = Blueprint('requerimientos_condiciones', __name__)

@requerimientos_condiciones_bp.route('/', methods=['GET'])
@token_required
def get_requerimientos_condiciones():
    relaciones = RequerimientosCondiciones.query.all()
    return jsonify([{
        "id_requerimiento": r.id_requerimiento,
        "id_condicion": r.id_condicion
    } for r in relaciones])

@requerimientos_condiciones_bp.route('/<int:id_requerimiento>/<int:id_condicion>', methods=['GET'])
@token_required
def get_requerimiento_condicion(id_requerimiento, id_condicion):
    relacion = RequerimientosCondiciones.query.get_or_404((id_requerimiento, id_condicion))
    return jsonify({
        "id_requerimiento": relacion.id_requerimiento,
        "id_condicion": relacion.id_condicion
    })

@requerimientos_condiciones_bp.route('/', methods=['POST'])
@token_required
def create_requerimiento_condicion():
    data = request.get_json()
    new_relacion = RequerimientosCondiciones(
        id_requerimiento=data.get('id_requerimiento'),
        id_condicion=data.get('id_condicion')
    )
    db.session.add(new_relacion)
    db.session.commit()
    return jsonify({"message": "Requerimiento condicion created", "id_requerimiento": new_relacion.id_requerimiento, "id_condicion": new_relacion.id_condicion}), 201

@requerimientos_condiciones_bp.route('/<int:id_requerimiento>/<int:id_condicion>', methods=['PUT'])
@token_required
def update_requerimiento_condicion(id_requerimiento, id_condicion):
    relacion = RequerimientosCondiciones.query.get_or_404((id_requerimiento, id_condicion))
    db.session.commit()  # No hay campos actualizables, solo eliminación o creación
    return jsonify({"message": "Requerimiento condicion unchanged"})

@requerimientos_condiciones_bp.route('/<int:id_requerimiento>/<int:id_condicion>', methods=['DELETE'])
@token_required
def delete_requerimiento_condicion(id_requerimiento, id_condicion):
    relacion = RequerimientosCondiciones.query.get_or_404((id_requerimiento, id_condicion))
    db.session.delete(relacion)
    db.session.commit()
    return jsonify({"message": "Requerimiento condicion deleted"})