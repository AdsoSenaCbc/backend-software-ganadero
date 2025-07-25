from flask import Blueprint, request, jsonify
from app import db
from app.models.ingrediente_materia_prima import IngredienteMateriaPrima
from app.utils.jwt_utils import token_required

ingrediente_materia_prima_bp = Blueprint('ingrediente_materia_prima', __name__)

@ingrediente_materia_prima_bp.route('/', methods=['GET'])
@token_required
def get_ingrediente_materia_primas():
    relaciones = IngredienteMateriaPrima.query.all()
    return jsonify([{
        "id_ingrediente": r.id_ingrediente,
        "id_materia": r.id_materia,
        "cantidad_kg": float(r.cantidad_kg)
    } for r in relaciones])

@ingrediente_materia_prima_bp.route('/<int:id_ingrediente>/<int:id_materia>', methods=['GET'])
@token_required
def get_ingrediente_materia_prima(id_ingrediente, id_materia):
    relacion = IngredienteMateriaPrima.query.get_or_404((id_ingrediente, id_materia))
    return jsonify({
        "id_ingrediente": relacion.id_ingrediente,
        "id_materia": relacion.id_materia,
        "cantidad_kg": float(relacion.cantidad_kg)
    })

@ingrediente_materia_prima_bp.route('/', methods=['POST'])
@token_required
def create_ingrediente_materia_prima():
    data = request.get_json()
    new_relacion = IngredienteMateriaPrima(
        id_ingrediente=data.get('id_ingrediente'),
        id_materia=data.get('id_materia'),
        cantidad_kg=data.get('cantidad_kg')
    )
    db.session.add(new_relacion)
    db.session.commit()
    return jsonify({"message": "Ingrediente materia prima created", "id_ingrediente": new_relacion.id_ingrediente, "id_materia": new_relacion.id_materia}), 201

@ingrediente_materia_prima_bp.route('/<int:id_ingrediente>/<int:id_materia>', methods=['PUT'])
@token_required
def update_ingrediente_materia_prima(id_ingrediente, id_materia):
    relacion = IngredienteMateriaPrima.query.get_or_404((id_ingrediente, id_materia))
    data = request.get_json()
    relacion.cantidad_kg = data.get('cantidad_kg', relacion.cantidad_kg)
    db.session.commit()
    return jsonify({"message": "Ingrediente materia prima updated"})

@ingrediente_materia_prima_bp.route('/<int:id_ingrediente>/<int:id_materia>', methods=['DELETE'])
@token_required
def delete_ingrediente_materia_prima(id_ingrediente, id_materia):
    relacion = IngredienteMateriaPrima.query.get_or_404((id_ingrediente, id_materia))
    db.session.delete(relacion)
    db.session.commit()
    return jsonify({"message": "Ingrediente materia prima deleted"})