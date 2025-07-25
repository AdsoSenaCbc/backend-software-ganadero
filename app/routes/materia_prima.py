from flask import Blueprint, request, jsonify
from app import db
from app.models.materia_prima import MateriaPrima
from app.utils.jwt_utils import token_required

materia_prima_bp = Blueprint('materia_prima', __name__)

@materia_prima_bp.route('/', methods=['GET'])
@token_required
def get_materias_primas():
    materias = MateriaPrima.query.all()
    return jsonify([{
        "id_materia": m.id_materia,
        "nombre": m.nombre,
        "fuente": m.fuente,
        "descripcion": m.descripcion
    } for m in materias])

@materia_prima_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_materia_prima(id):
    materia = MateriaPrima.query.get_or_404(id)
    return jsonify({
        "id_materia": materia.id_materia,
        "nombre": materia.nombre,
        "fuente": materia.fuente,
        "descripcion": materia.descripcion
    })

@materia_prima_bp.route('/', methods=['POST'])
@token_required
def create_materia_prima():
    data = request.get_json()
    new_materia = MateriaPrima(
        nombre=data.get('nombre'),
        fuente=data.get('fuente'),
        descripcion=data.get('descripcion')
    )
    db.session.add(new_materia)
    db.session.commit()
    return jsonify({"message": "Materia prima created", "id": new_materia.id_materia}), 201

@materia_prima_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_materia_prima(id):
    materia = MateriaPrima.query.get_or_404(id)
    data = request.get_json()
    materia.nombre = data.get('nombre', materia.nombre)
    materia.fuente = data.get('fuente', materia.fuente)
    materia.descripcion = data.get('descripcion', materia.descripcion)
    db.session.commit()
    return jsonify({"message": "Materia prima updated"})

@materia_prima_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_materia_prima(id):
    materia = MateriaPrima.query.get_or_404(id)
    db.session.delete(materia)
    db.session.commit()
    return jsonify({"message": "Materia prima deleted"})