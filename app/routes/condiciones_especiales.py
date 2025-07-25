from flask import Blueprint, request, jsonify
from app import db
from app.models.condiciones_especiales import CondicionesEspeciales
from app.utils.jwt_utils import token_required

condiciones_especiales_bp = Blueprint('condiciones_especiales', __name__)

@condiciones_especiales_bp.route('/', methods=['GET'])
@token_required
def index():
    condiciones = CondicionesEspeciales.query.all()
    return jsonify([{
        "id_condicion": c.id_condicion,
        "nombre": c.nombre,
        "descripcion": c.descripcion,
        "ajuste_nutriente": float(c.ajuste_nutriente)
    } for c in condiciones])

@condiciones_especiales_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_condicion_especial(id):
    condicion = CondicionesEspeciales.query.get_or_404(id)
    return jsonify({
        "id_condicion": condicion.id_condicion,
        "nombre": condicion.nombre,
        "descripcion": condicion.descripcion,
        "ajuste_nutriente": float(condicion.ajuste_nutriente)
    })

@condiciones_especiales_bp.route('/', methods=['POST'])
@token_required
def create_condicion_especial():
    data = request.get_json()
    new_condicion = CondicionesEspeciales(
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion'),
        ajuste_nutriente=data.get('ajuste_nutriente')
    )
    db.session.add(new_condicion)
    db.session.commit()
    return jsonify({"message": "Condicion especial created", "id": new_condicion.id_condicion}), 201

@condiciones_especiales_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_condicion_especial(id):
    condicion = CondicionesEspeciales.query.get_or_404(id)
    data = request.get_json()
    condicion.nombre = data.get('nombre', condicion.nombre)
    condicion.descripcion = data.get('descripcion', condicion.descripcion)
    condicion.ajuste_nutriente = data.get('ajuste_nutriente', condicion.ajuste_nutriente)
    db.session.commit()
    return jsonify({"message": "Condicion especial updated"})

@condiciones_especiales_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_condicion_especial(id):
    condicion = CondicionesEspeciales.query.get_or_404(id)
    db.session.delete(condicion)
    db.session.commit()
    return jsonify({"message": "Condicion especial deleted"})