from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.requerimientos_condiciones import RequerimientosCondiciones
from app.utils.jwt_utils import token_required

requerimientos_condiciones_bp = Blueprint('requerimientos_condiciones', __name__)

# --------------------------
# API JSON ENDPOINTS
# --------------------------

@requerimientos_condiciones_bp.route('/api', methods=['GET'])
@token_required
def get_requerimientos_api():
    relaciones = RequerimientosCondiciones.query.all()
    return jsonify([{
        "id_requerimiento": r.id_requerimiento,
        "id_condicion": r.id_condicion
    } for r in relaciones])

@requerimientos_condiciones_bp.route('/api/<int:id_requerimiento>/<int:id_condicion>', methods=['GET'])
@token_required
def get_requerimiento_api(id_requerimiento, id_condicion):
    relacion = RequerimientosCondiciones.query.get_or_404((id_requerimiento, id_condicion))
    return jsonify({
        "id_requerimiento": relacion.id_requerimiento,
        "id_condicion": relacion.id_condicion
    })

@requerimientos_condiciones_bp.route('/api', methods=['POST'])
@token_required
def create_requerimiento_condicion():
    data = request.get_json()
    new_relacion = RequerimientosCondiciones(
        id_requerimiento=data.get('id_requerimiento'),
        id_condicion=data.get('id_condicion')
    )
    db.session.add(new_relacion)
    db.session.commit()
    return jsonify({"message": "Requerimiento condicion created", "id_requerimiento": new_relacion.id_requerimiento, "id_condicion": new_relacion.id_condicion}), 201

@requerimientos_condiciones_bp.route('/api/<int:id_requerimiento>/<int:id_condicion>', methods=['PUT'])
@token_required
def update_requerimiento_condicion(id_requerimiento, id_condicion):
    relacion = RequerimientosCondiciones.query.get_or_404((id_requerimiento, id_condicion))
    db.session.commit()  # No hay campos actualizables, solo eliminación o creación
    return jsonify({"message": "Requerimiento condicion unchanged"})

@requerimientos_condiciones_bp.route('/api/<int:id_requerimiento>/<int:id_condicion>', methods=['DELETE'])
@token_required
def delete_requerimiento_condicion(id_requerimiento, id_condicion):
    relacion = RequerimientosCondiciones.query.get_or_404((id_requerimiento, id_condicion))
    db.session.delete(relacion)
    db.session.commit()
    return jsonify({"message": "Requerimiento condicion deleted"})

# --------------------------
# HTML CRUD ROUTES
# --------------------------
from flask_login import login_required

@requerimientos_condiciones_bp.route('/', methods=['GET'])
@login_required
def index_html():
    relaciones = RequerimientosCondiciones.query.all()
    return render_template('requerimientos_condiciones/index.html', relaciones=relaciones)

@requerimientos_condiciones_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_html():
    if request.method == 'POST':
        data = request.form
        nueva = RequerimientosCondiciones(
            id_requerimiento=data.get('id_requerimiento'),
            id_condicion=data.get('id_condicion')
        )
        db.session.add(nueva)
        db.session.commit()
        flash('Relación creada.', 'success')
        return redirect(url_for('requerimientos_condiciones.index_html'))
    return render_template('requerimientos_condiciones/create.html')

@requerimientos_condiciones_bp.route('/<int:id_requerimiento>/<int:id_condicion>/delete', methods=['GET', 'POST'])
@login_required
def delete_html(id_requerimiento, id_condicion):
    rel = RequerimientosCondiciones.query.get_or_404((id_requerimiento, id_condicion))
    if request.method == 'POST':
        db.session.delete(rel)
        db.session.commit()
        flash('Relación eliminada.', 'success')
        return redirect(url_for('requerimientos_condiciones.index_html'))
    return render_template('requerimientos_condiciones/delete.html', rel=rel)

@requerimientos_condiciones_bp.route('/<int:id_requerimiento>/<int:id_condicion>/update', methods=['GET', 'POST'])
@login_required
def update_html(id_requerimiento, id_condicion):
    rel = RequerimientosCondiciones.query.get_or_404((id_requerimiento, id_condicion))
    if request.method == 'POST':
        data = request.form
        # En este caso solo permitimos cambiar los IDs (no recomendado) pero se mantiene para consistencia
        rel.id_requerimiento = data.get('id_requerimiento', rel.id_requerimiento)
        rel.id_condicion = data.get('id_condicion', rel.id_condicion)
        db.session.commit()
        flash('Relación actualizada.', 'success')
        return redirect(url_for('requerimientos_condiciones.index_html'))
    return render_template('requerimientos_condiciones/update.html', rel=rel)