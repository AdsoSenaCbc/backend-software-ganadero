from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.racion import Racion
from app.models.animal import Animal
from app.models.requerimientos_nutricionales import RequerimientosNutricionales
from app.utils.jwt_utils import token_required

racion_bp = Blueprint('racion', __name__, url_prefix='/racion')

# --------------------------
# API JSON ENDPOINTS
# --------------------------

@racion_bp.route('/api', methods=['GET'])
@token_required
def get_raciones_api():
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

@racion_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_racion_api(id):
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

@racion_bp.route('/api', methods=['POST'])
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

@racion_bp.route('/api/<int:id>', methods=['PUT'])
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

@racion_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_racion(id):
    racion = Racion.query.get_or_404(id)
    db.session.delete(racion)
    db.session.commit()

    return jsonify({"message": "Racion deleted"})

# --------------------------
# HTML CRUD ROUTES
# --------------------------
from flask_login import login_required

@racion_bp.route('/', methods=['GET'])
@login_required
def index_html():
    raciones = Racion.query.all()
    return render_template('racion/index.html', raciones=raciones)

@racion_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_html():
    if request.method == 'POST':
        data = request.form
        nueva = Racion(
            id_animal=data.get('id_animal'),
            id_requerimiento=data.get('id_requerimiento'),
            ms_total=data.get('ms_total'),
            calculado_por=data.get('calculado_por'),
            observaciones=data.get('observaciones')
        )
        db.session.add(nueva)
        db.session.commit()
        flash('Ración creada.', 'success')
        return redirect(url_for('racion.index_html'))
    return render_template('racion/create.html')

@racion_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_html(id):
    rac = Racion.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        rac.id_animal = data.get('id_animal', rac.id_animal)
        rac.id_requerimiento = data.get('id_requerimiento', rac.id_requerimiento)
        rac.ms_total = data.get('ms_total', rac.ms_total)
        rac.calculado_por = data.get('calculado_por', rac.calculado_por)
        rac.observaciones = data.get('observaciones', rac.observaciones)
        db.session.commit()
        flash('Ración actualizada.', 'success')
        return redirect(url_for('racion.index_html'))
    return render_template('racion/update.html', rac=rac)

@racion_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_html(id):
    rac = Racion.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(rac)
        db.session.commit()
        flash('Ración eliminada.', 'success')
        return redirect(url_for('racion.index_html'))
    return render_template('racion/delete.html', rac=rac)
