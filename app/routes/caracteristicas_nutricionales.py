from flask import Blueprint, request, jsonify
from app import db
from app.models.caracteristicas_nutricionales import CaracteristicasNutricionales
from app.utils.jwt_utils import token_required

caracteristicas_nutricionales_bp = Blueprint('caracteristicas_nutricionales', __name__)

@caracteristicas_nutricionales_bp.route('/', methods=['GET'])
@token_required
def index():
    caracteristicas = CaracteristicasNutricionales.query.all()
    return jsonify([{
        "id_caracteristica": c.id_caracteristica,
        "id_ingrediente": c.id_ingrediente,
        "id_nutriente": c.id_nutriente,
        "valor": float(c.valor)
    } for c in caracteristicas])

@caracteristicas_nutricionales_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_caracteristica_nutricional(id):
    caracteristica = CaracteristicasNutricionales.query.get_or_404(id)
    return jsonify({
        "id_caracteristica": caracteristica.id_caracteristica,
        "id_ingrediente": caracteristica.id_ingrediente,
        "id_nutriente": caracteristica.id_nutriente,
        "valor": float(caracteristica.valor)
    })

@caracteristicas_nutricionales_bp.route('/', methods=['POST'])
@token_required
def create_caracteristica_nutricional():
    data = request.get_json()
    new_caracteristica = CaracteristicasNutricionales(
        id_ingrediente=data.get('id_ingrediente'),
        id_nutriente=data.get('id_nutriente'),
        valor=data.get('valor')
    )
    db.session.add(new_caracteristica)
    db.session.commit()
    return jsonify({"message": "Caracteristica nutricional created", "id": new_caracteristica.id_caracteristica}), 201

@caracteristicas_nutricionales_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_caracteristica_nutricional(id):
    caracteristica = CaracteristicasNutricionales.query.get_or_404(id)
    data = request.get_json()
    caracteristica.id_ingrediente = data.get('id_ingrediente', caracteristica.id_ingrediente)
    caracteristica.id_nutriente = data.get('id_nutriente', caracteristica.id_nutriente)
    caracteristica.valor = data.get('valor', caracteristica.valor)
    db.session.commit()
    return jsonify({"message": "Caracteristica nutricional updated"})

@caracteristicas_nutricionales_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_caracteristica_nutricional(id):
    caracteristica = CaracteristicasNutricionales.query.get_or_404(id)
    db.session.delete(caracteristica)
    db.session.commit()
    return jsonify({"message": "Caracteristica nutricional deleted"})