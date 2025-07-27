from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.detalle_racion_nutricional import DetalleRacionNutricional
from app.models.racion import Racion
from app.models.nutrientes import Nutrientes
from app.utils.jwt_utils import token_required

detalle_racion_nutricional_bp = Blueprint('detalle_racion_nutricional', __name__, url_prefix='/detalle-racion-nutricional')

@detalle_racion_nutricional_bp.route('/', methods=['GET'])
@token_required
def get_detalle_racion_nutricionales():
    detalles = DetalleRacionNutricional.query.all()
    return jsonify([{
        "id_detalle_nut": d.id_detalle_nut,
        "id_racion": d.id_racion,
        "id_nutriente": d.id_nutriente,
        "valor_aportado": float(d.valor_aportado)
    } for d in detalles])

@detalle_racion_nutricional_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_detalle_racion_nutricional(id):
    detalle = DetalleRacionNutricional.query.get_or_404(id)
    return jsonify({
        "id_detalle_nut": detalle.id_detalle_nut,
        "id_racion": detalle.id_racion,
        "id_nutriente": detalle.id_nutriente,
        "valor_aportado": float(detalle.valor_aportado)
    })

@detalle_racion_nutricional_bp.route('/', methods=['POST'])
@token_required
def create_detalle_racion_nutricional():
    data = request.get_json()
    new_detalle = DetalleRacionNutricional(
        id_racion=data.get('id_racion'),
        id_nutriente=data.get('id_nutriente'),
        valor_aportado=data.get('valor_aportado')
    )
    db.session.add(new_detalle)
    db.session.commit()
    return jsonify({"message": "Detalle racion nutricional created", "id": new_detalle.id_detalle_nut}), 201

@detalle_racion_nutricional_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_detalle_racion_nutricional(id):
    detalle = DetalleRacionNutricional.query.get_or_404(id)
    data = request.get_json()
    detalle.id_racion = data.get('id_racion', detalle.id_racion)
    detalle.id_nutriente = data.get('id_nutriente', detalle.id_nutriente)
    detalle.valor_aportado = data.get('valor_aportado', detalle.valor_aportado)
    db.session.commit()
    return jsonify({"message": "Detalle racion nutricional updated"})

@detalle_racion_nutricional_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_detalle_racion_nutricional(id):
    detalle = DetalleRacionNutricional.query.get_or_404(id)
    db.session.delete(detalle)
    db.session.commit()
    return jsonify({"message": "Detalle de ración nutricional eliminado"})

# ==============================================
# RUTAS WEB
# ==============================================

@detalle_racion_nutricional_bp.route('/web', methods=['GET'])
@detalle_racion_nutricional_bp.route('/', methods=['GET'])
@login_required
def index():
    detalles = db.session.query(
        DetalleRacionNutricional,
        Racion,
        Nutrientes.nombre.label('nombre_nutriente')
    ).join(
        Racion,
        DetalleRacionNutricional.id_racion == Racion.id_racion
    ).join(
        Nutrientes,
        DetalleRacionNutricional.id_nutriente == Nutrientes.id_nutriente
    ).all()
    
    return render_template('detalle_racion_nutricional/index.html', 
                         detalles=detalles)