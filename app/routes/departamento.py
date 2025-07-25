from flask import Blueprint, request, jsonify
from app import db
from app.models.departamento import Departamento
from app.utils.jwt_utils import token_required

departamento_bp = Blueprint('departamento', __name__)

@departamento_bp.route('/', methods=['GET'])
@token_required
def get_departamentos():
    departamentos = Departamento.query.all()
    return jsonify([{
        "id_departamento": d.id_departamento,
        "nombre_departamento": d.nombre_departamento
    } for d in departamentos])

@departamento_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_departamento(id):
    departamento = Departamento.query.get_or_404(id)
    return jsonify({
        "id_departamento": departamento.id_departamento,
        "nombre_departamento": departamento.nombre_departamento
    })

@departamento_bp.route('/', methods=['POST'])
@token_required
def create_departamento():
    data = request.get_json()
    new_departamento = Departamento(
        nombre_departamento=data.get('nombre_departamento')
    )
    db.session.add(new_departamento)
    db.session.commit()
    return jsonify({"message": "Departamento created", "id": new_departamento.id_departamento}), 201

@departamento_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_departamento(id):
    departamento = Departamento.query.get_or_404(id)
    data = request.get_json()
    departamento.nombre_departamento = data.get('nombre_departamento', departamento.nombre_departamento)
    db.session.commit()
    return jsonify({"message": "Departamento updated"})

@departamento_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_departamento(id):
    departamento = Departamento.query.get_or_404(id)
    db.session.delete(departamento)
    db.session.commit()
    return jsonify({"message": "Departamento deleted"})

# Alias para el panel de control: endpoint departamento.index
# Registra la misma URL '/' pero con nombre de endpoint 'index' para evitar BuildError.
departamento_bp.add_url_rule('/', endpoint='index', view_func=get_departamentos, methods=['GET'])