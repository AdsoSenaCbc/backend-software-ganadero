from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.historial_hacienda import HistorialHacienda
from app.models.hacienda import Hacienda
from app.utils.jwt_utils import token_required
from flask_login import login_required

historial_hacienda_bp = Blueprint('historial_hacienda', __name__)

# API CRUD ROUTES
@historial_hacienda_bp.route('/api', methods=['GET'])
@token_required
def get_historiales_api():
    historiales = HistorialHacienda.query.all()
    return jsonify([{
        "id_historial": h.id_historial,
        "id_hacienda": h.id_hacienda,
        "fecha": h.fecha.isoformat(),
        "existencia_animales": float(h.existencia_animales),
        "area": float(h.area),
        "estado": h.estado,
        "observaciones": h.observaciones
    } for h in historiales])

@historial_hacienda_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_historial_api(id):
    historial = HistorialHacienda.query.get_or_404(id)
    return jsonify({
        "id_historial": historial.id_historial,
        "id_hacienda": historial.id_hacienda,
        "fecha": historial.fecha.isoformat(),
        "existencia_animales": float(historial.existencia_animales),
        "area": float(historial.area),
        "estado": historial.estado,
        "observaciones": historial.observaciones
    })

@historial_hacienda_bp.route('/api', methods=['POST'])
@token_required
def create_historial_hacienda():
    data = request.get_json()
    new_historial = HistorialHacienda(
        id_hacienda=data.get('id_hacienda'),
        existencia_animales=data.get('existencia_animales'),
        area=data.get('area'),
        estado=data.get('estado'),
        observaciones=data.get('observaciones')
    )
    db.session.add(new_historial)
    db.session.commit()
    return jsonify({"message": "Historial hacienda created", "id": new_historial.id_historial}), 201

@historial_hacienda_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_historial_hacienda(id):
    historial = HistorialHacienda.query.get_or_404(id)
    data = request.get_json()
    historial.id_hacienda = data.get('id_hacienda', historial.id_hacienda)
    historial.existencia_animales = data.get('existencia_animales', historial.existencia_animales)
    historial.area = data.get('area', historial.area)
    historial.estado = data.get('estado', historial.estado)
    historial.observaciones = data.get('observaciones', historial.observaciones)
    db.session.commit()
    return jsonify({"message": "Historial hacienda updated"})

@historial_hacienda_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_historial_hacienda(id):
    historial = HistorialHacienda.query.get_or_404(id)
    db.session.delete(historial)
    db.session.commit()
    return jsonify({"message": "Historial hacienda deleted"})

# HTML CRUD ROUTES
@historial_hacienda_bp.route('/', methods=['GET'])
@login_required
def index_html():
    historiales = HistorialHacienda.query.all()
    haciendas_lookup = {h.id_hacienda: h for h in Hacienda.query.all()}
    return render_template('historial_hacienda/index.html', historiales=historiales, haciendas_lookup=haciendas_lookup)

@historial_hacienda_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_html():
    if request.method == 'POST':
        data = request.form
        nuevo = HistorialHacienda(
            id_hacienda=data.get('id_hacienda'),
            fecha=data.get('fecha'),
            existencia_animales=data.get('existencia_animales'),
            area=data.get('area'),
            estado=data.get('estado'),
            observaciones=data.get('observaciones')
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Historial de hacienda creado.', 'success')
        return redirect(url_for('historial_hacienda.index_html'))
    haciendas = Hacienda.query.all()
    return render_template('historial_hacienda/create.html', haciendas=haciendas)

@historial_hacienda_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_html(id):
    hist = HistorialHacienda.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        hist.id_hacienda = data.get('id_hacienda', hist.id_hacienda)
        hist.fecha = data.get('fecha', hist.fecha)
        hist.existencia_animales = data.get('existencia_animales', hist.existencia_animales)
        hist.area = data.get('area', hist.area)
        hist.estado = data.get('estado', hist.estado)
        hist.observaciones = data.get('observaciones', hist.observaciones)
        db.session.commit()
        flash('Historial de hacienda actualizado.', 'success')
        return redirect(url_for('historial_hacienda.index_html'))
    haciendas = Hacienda.query.all()
    return render_template('historial_hacienda/update.html', hist=hist, haciendas=haciendas)

@historial_hacienda_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_html(id):
    hist = HistorialHacienda.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(hist)
        db.session.commit()
        flash('Historial de hacienda eliminado.', 'success')
        return redirect(url_for('historial_hacienda.index_html'))
    return render_template('historial_hacienda/delete.html', hist=hist)