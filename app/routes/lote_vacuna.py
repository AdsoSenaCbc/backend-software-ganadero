from flask import Blueprint, request, jsonify
from app import db
from app.models.lote_vacuna import LoteVacuna
from app.utils.jwt_utils import token_required

lote_vacuna_bp = Blueprint('lote_vacuna', __name__)

@lote_vacuna_bp.route('/', methods=['GET'])
@token_required
def get_lotes_vacuna():
    lotes = LoteVacuna.query.all()
    return jsonify([{
        "id_lote": l.id_lote,
        "codigo_lote": l.codigo_lote,
        "fecha_vencimiento": l.fecha_vencimiento.isoformat() if l.fecha_vencimiento else None,
        "fabricante": l.fabricante
    } for l in lotes])

@lote_vacuna_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_lote_vacuna(id):
    lote = LoteVacuna.query.get_or_404(id)
    return jsonify({
        "id_lote": lote.id_lote,
        "codigo_lote": lote.codigo_lote,
        "fecha_vencimiento": lote.fecha_vencimiento.isoformat() if lote.fecha_vencimiento else None,
        "fabricante": lote.fabricante
    })

@lote_vacuna_bp.route('/', methods=['POST'])
@token_required
def create_lote_vacuna():
    data = request.get_json()
    new_lote = LoteVacuna(
        codigo_lote=data.get('codigo_lote'),
        fecha_vencimiento=data.get('fecha_vencimiento'),
        fabricante=data.get('fabricante')
    )
    db.session.add(new_lote)
    db.session.commit()
    return jsonify({"message": "Lote vacuna created", "id": new_lote.id_lote}), 201

@lote_vacuna_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_lote_vacuna(id):
    lote = LoteVacuna.query.get_or_404(id)
    data = request.get_json()
    lote.codigo_lote = data.get('codigo_lote', lote.codigo_lote)
    lote.fecha_vencimiento = data.get('fecha_vencimiento', lote.fecha_vencimiento)
    lote.fabricante = data.get('fabricante', lote.fabricante)
    db.session.commit()
    return jsonify({"message": "Lote vacuna updated"})

@lote_vacuna_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_lote_vacuna(id):
    lote = LoteVacuna.query.get_or_404(id)
    db.session.delete(lote)
    db.session.commit()
    return jsonify({"message": "Lote vacuna deleted"})