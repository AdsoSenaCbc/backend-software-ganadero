from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.racion import Racion
from app.models.animal import Animal
from app.models.requerimientos_nutricionales import RequerimientosNutricionales
from app.utils.jwt_utils import token_required

racion_bp = Blueprint('racion', __name__, url_prefix='/racion')

@racion_bp.route('/', methods=['GET'])
@token_required
def get_raciones():
    raciones = Racion.query.all()
    return jsonify([{
        "id_racion": r.id_racion,
        "id_animal": r.id_animal,
        "id_requerimiento": r.id_requerimiento,
        "fecha_calculo": r.fecha_calculo.isoformat(),
        "ms_total": float(r.ms_total),
        "calculado_por": r.calculado_por,
        "observaciones": r.observaciones
    } for r in raciones])

@racion_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_racion(id):
    racion = Racion.query.get_or_404(id)
    return jsonify({
        "id_racion": racion.id_racion,
        "id_animal": racion.id_animal,
        "id_requerimiento": racion.id_requerimiento,
        "fecha_calculo": racion.fecha_calculo.isoformat(),
        "ms_total": float(racion.ms_total),
        "calculado_por": racion.calculado_por,
        "observaciones": racion.observaciones
    })

@racion_bp.route('/', methods=['POST'])
@token_required
def create_racion():
    data = request.get_json()
    new_racion = Racion(
        id_animal=data.get('id_animal'),
        id_requerimiento=data.get('id_requerimiento'),
        ms_total=data.get('ms_total'),
        calculado_por=data.get('calculado_por'),
        observaciones=data.get('observaciones')
    )
    db.session.add(new_racion)
    db.session.commit()
    return jsonify({"message": "Racion created", "id": new_racion.id_racion}), 201

@racion_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_racion(id):
    racion = Racion.query.get_or_404(id)
    data = request.get_json()
    racion.id_animal = data.get('id_animal', racion.id_animal)
    racion.id_requerimiento = data.get('id_requerimiento', racion.id_requerimiento)
    racion.ms_total = data.get('ms_total', racion.ms_total)
    racion.calculado_por = data.get('calculado_por', racion.calculado_por)
    racion.observaciones = data.get('observaciones', racion.observaciones)
    db.session.commit()
    return jsonify({"message": "Racion updated"})

@racion_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_racion(id):
    racion = Racion.query.get_or_404(id)
    db.session.delete(racion)
    db.session.commit()
    return jsonify({"message": "Ración eliminada"})

# ==============================================
# RUTAS WEB
# ==============================================

@racion_bp.route('/web', methods=['GET'])
@racion_bp.route('/', methods=['GET'])
@login_required
def index():
    raciones = db.session.query(
        Racion,
        Animal.identificacion.label('identificacion_animal'),
        Animal.nombre.label('nombre_animal')
    ).join(
        Animal,
        Racion.id_animal == Animal.id_animal
    ).all()
    
    return render_template('racion/index.html', 
                         raciones=raciones)