from flask import Blueprint, request, jsonify
from app import db
from app.models.vacuna import Vacuna
from app.utils.jwt_utils import token_required

vacuna_bp = Blueprint('vacuna', __name__)

@vacuna_bp.route('/', methods=['GET'])
@token_required
def get_vacunas():
    vacunas = Vacuna.query.all()
    return jsonify([{
        "id_vacuna": v.id_vacuna,
        "nombre": v.nombre,
        "tipo": v.tipo,
        "descripcion": v.descripcion,
        "dosis_recomendada": v.dosis_recomendada
    } for v in vacunas])

@vacuna_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_vacuna(id):
    vacuna = Vacuna.query.get_or_404(id)
    return jsonify({
        "id_vacuna": vacuna.id_vacuna,
        "nombre": vacuna.nombre,
        "tipo": vacuna.tipo,
        "descripcion": vacuna.descripcion,
        "dosis_recomendada": vacuna.dosis_recomendada
    })

@vacuna_bp.route('/', methods=['POST'])
@token_required
def create_vacuna():
    data = request.get_json()
    new_vacuna = Vacuna(
        nombre=data.get('nombre'),
        tipo=data.get('tipo'),
        descripcion=data.get('descripcion'),
        dosis_recomendada=data.get('dosis_recomendada')
    )
    db.session.add(new_vacuna)
    db.session.commit()
    return jsonify({"message": "Vacuna created", "id": new_vacuna.id_vacuna}), 201

@vacuna_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_vacuna(id):
    vacuna = Vacuna.query.get_or_404(id)
    data = request.get_json()
    vacuna.nombre = data.get('nombre', vacuna.nombre)
    vacuna.tipo = data.get('tipo', vacuna.tipo)
    vacuna.descripcion = data.get('descripcion', vacuna.descripcion)
    vacuna.dosis_recomendada = data.get('dosis_recomendada', vacuna.dosis_recomendada)
    db.session.commit()
    return jsonify({"message": "Vacuna updated"})

@vacuna_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_vacuna(id):
    vacuna = Vacuna.query.get_or_404(id)
    db.session.delete(vacuna)
    db.session.commit()
    return jsonify({"message": "Vacuna deleted"})