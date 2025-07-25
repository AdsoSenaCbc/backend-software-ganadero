from flask import Blueprint, request, jsonify
from app import db
from app.models.requerimientos_nrc import RequerimientosNrc
from app.utils.jwt_utils import token_required

requerimientos_nrc_bp = Blueprint('requerimientos_nrc', __name__)

@requerimientos_nrc_bp.route('/', methods=['GET'])
@token_required
def get_requerimientos_nrc():
    requerimientos = RequerimientosNrc.query.all()
    return jsonify([{
        "id": r.id,
        "etapa": r.etapa,
        "peso": float(r.peso),
        "produccion_leche": float(r.produccion_leche),
        "grasa_leche": float(r.grasa_leche),
        "em": float(r.em),
        "pc": float(r.pc),
        "ms": float(r.ms),
        "observaciones": r.observaciones
    } for r in requerimientos])

@requerimientos_nrc_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_requerimiento_nrc(id):
    requerimiento = RequerimientosNrc.query.get_or_404(id)
    return jsonify({
        "id": requerimiento.id,
        "etapa": requerimiento.etapa,
        "peso": float(requerimiento.peso),
        "produccion_leche": float(requerimiento.produccion_leche),
        "grasa_leche": float(requerimiento.grasa_leche),
        "em": float(requerimiento.em),
        "pc": float(requerimiento.pc),
        "ms": float(requerimiento.ms),
        "observaciones": requerimiento.observaciones
    })

@requerimientos_nrc_bp.route('/', methods=['POST'])
@token_required
def create_requerimiento_nrc():
    data = request.get_json()
    new_requerimiento = RequerimientosNrc(
        etapa=data.get('etapa'),
        peso=data.get('peso'),
        produccion_leche=data.get('produccion_leche'),
        grasa_leche=data.get('grasa_leche'),
        em=data.get('em'),
        pc=data.get('pc'),
        ms=data.get('ms'),
        observaciones=data.get('observaciones')
    )
    db.session.add(new_requerimiento)
    db.session.commit()
    return jsonify({"message": "Requerimiento NRC created", "id": new_requerimiento.id}), 201

@requerimientos_nrc_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_requerimiento_nrc(id):
    requerimiento = RequerimientosNrc.query.get_or_404(id)
    data = request.get_json()
    requerimiento.etapa = data.get('etapa', requerimiento.etapa)
    requerimiento.peso = data.get('peso', requerimiento.peso)
    requerimiento.produccion_leche = data.get('produccion_leche', requerimiento.produccion_leche)
    requerimiento.grasa_leche = data.get('grasa_leche', requerimiento.grasa_leche)
    requerimiento.em = data.get('em', requerimiento.em)
    requerimiento.pc = data.get('pc', requerimiento.pc)
    requerimiento.ms = data.get('ms', requerimiento.ms)
    requerimiento.observaciones = data.get('observaciones', requerimiento.observaciones)
    db.session.commit()
    return jsonify({"message": "Requerimiento NRC updated"})

@requerimientos_nrc_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_requerimiento_nrc(id):
    requerimiento = RequerimientosNrc.query.get_or_404(id)
    db.session.delete(requerimiento)
    db.session.commit()
    return jsonify({"message": "Requerimiento NRC deleted"})