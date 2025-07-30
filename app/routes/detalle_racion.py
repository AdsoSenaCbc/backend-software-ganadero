from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.detalle_racion import DetalleRacion
from app.utils.jwt_utils import token_required

detalle_racion_bp = Blueprint('detalle_racion', __name__)

# --------------------------
# API JSON ENDPOINTS
# --------------------------

@detalle_racion_bp.route('/api', methods=['GET'])
@token_required
def get_detalles_api():
    detalles = DetalleRacion.query.all()
    return jsonify([{
        "id_detalle": d.id_detalle,
        "id_racion": d.id_racion,
        "id_ingrediente": d.id_ingrediente,
        "cantidad_kg": float(d.cantidad_kg),
        "porcentaje_ms": float(d.porcentaje_ms)
    } for d in detalles])

@detalle_racion_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_detalle_api(id):
    detalle = DetalleRacion.query.get_or_404(id)
    return jsonify({
        "id_detalle": detalle.id_detalle,
        "id_racion": detalle.id_racion,
        "id_ingrediente": detalle.id_ingrediente,
        "cantidad_kg": float(detalle.cantidad_kg),
        "porcentaje_ms": float(detalle.porcentaje_ms)
    })

@detalle_racion_bp.route('/api', methods=['POST'])
@token_required
def create_detalle_racion():
    data = request.get_json()
    new_detalle = DetalleRacion(
        id_racion=data.get('id_racion'),
        id_ingrediente=data.get('id_ingrediente'),
        cantidad_kg=data.get('cantidad_kg'),
        porcentaje_ms=data.get('porcentaje_ms')
    )
    db.session.add(new_detalle)
    db.session.commit()
    return jsonify({"message": "Detalle racion created", "id": new_detalle.id_detalle}), 201

@detalle_racion_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_detalle_racion(id):
    detalle = DetalleRacion.query.get_or_404(id)
    data = request.get_json()
    detalle.id_racion = data.get('id_racion', detalle.id_racion)
    detalle.id_ingrediente = data.get('id_ingrediente', detalle.id_ingrediente)
    detalle.cantidad_kg = data.get('cantidad_kg', detalle.cantidad_kg)
    detalle.porcentaje_ms = data.get('porcentaje_ms', detalle.porcentaje_ms)
    db.session.commit()
    return jsonify({"message": "Detalle racion updated"})

@detalle_racion_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_detalle_racion(id):
    detalle = DetalleRacion.query.get_or_404(id)
    db.session.delete(detalle)
    db.session.commit()
    return jsonify({"message": "Detalle racion deleted"})

# --------------------------
# HTML CRUD ROUTES
# --------------------------
from flask_login import login_required

@detalle_racion_bp.route('/', methods=['GET'])
@login_required
def index_html():
    detalles = DetalleRacion.query.all()
    return render_template('detalle_racion/index.html', detalles=detalles)

@detalle_racion_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_html():
    if request.method == 'POST':
        data = request.form
        nuevo = DetalleRacion(
            id_racion=data.get('id_racion'),
            id_ingrediente=data.get('id_ingrediente'),
            cantidad_kg=data.get('cantidad_kg'),
            porcentaje_ms=data.get('porcentaje_ms')
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Detalle de ración creado.', 'success')
        return redirect(url_for('detalle_racion.index_html'))
    return render_template('detalle_racion/create.html')

@detalle_racion_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_html(id):
    det = DetalleRacion.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        det.id_racion = data.get('id_racion', det.id_racion)
        det.id_ingrediente = data.get('id_ingrediente', det.id_ingrediente)
        det.cantidad_kg = data.get('cantidad_kg', det.cantidad_kg)
        det.porcentaje_ms = data.get('porcentaje_ms', det.porcentaje_ms)
        db.session.commit()
        flash('Detalle de ración actualizado.', 'success')
        return redirect(url_for('detalle_racion.index_html'))
    return render_template('detalle_racion/update.html', det=det)

@detalle_racion_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_html(id):
    det = DetalleRacion.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(det)
        db.session.commit()
        flash('Detalle de ración eliminado.', 'success')
        return redirect(url_for('detalle_racion.index_html'))
    return render_template('detalle_racion/delete.html', det=det)