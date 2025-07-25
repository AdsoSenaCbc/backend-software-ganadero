from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.hacienda import Hacienda
from app.utils.jwt_utils import token_required

hacienda_bp = Blueprint('hacienda', __name__)

# --------------------------
# API JSON ENDPOINTS
# --------------------------

@hacienda_bp.route('/api', methods=['GET'])
@token_required
def get_haciendas_api():
    """Retorna la lista de haciendas en formato JSON"""
    haciendas = Hacienda.query.all()
    return jsonify([{"id": h.id_hacienda, "nombre": h.nombre} for h in haciendas])

@hacienda_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_hacienda_api(id):
    """Retorna una sola hacienda en formato JSON"""
    hacienda = Hacienda.query.get_or_404(id)
    return jsonify({
        "id": hacienda.id_hacienda,
        "nombre": hacienda.nombre,
        "tel_contacto": hacienda.tel_contacto,
        "ubicacion": hacienda.ubicacion,
        "descripcion": hacienda.descripcion,
        "id_departamento": hacienda.id_departamento,
        "id_municipio": hacienda.id_municipio,
        "id_usuario": hacienda.id_usuario,
    })

# --------------------------
# VISTAS HTML (CRUD)
# --------------------------
from flask_login import login_required  # importamos aquí para evitar ciclo si login no siempre se usa

@hacienda_bp.route('/', methods=['GET'])
@login_required
def index():
    """Vista principal que muestra todas las haciendas"""
    haciendas = Hacienda.query.all()
    return render_template('hacienda/index.html', haciendas=haciendas)


@hacienda_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        data = request.form
        new_hacienda = Hacienda(
            nombre=data.get('nombre'),
            tel_contacto=data.get('tel_contacto'),
            ubicacion=data.get('ubicacion'),
            descripcion=data.get('descripcion'),
            id_departamento=data.get('id_departamento'),
            id_municipio=data.get('id_municipio'),
            id_usuario=data.get('id_usuario')
        )
        db.session.add(new_hacienda)
        db.session.commit()
        flash('Hacienda creada exitosamente.', 'success')
        return redirect(url_for('hacienda.index'))
    return render_template('hacienda/create.html')


@hacienda_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    hacienda = Hacienda.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        hacienda.nombre = data.get('nombre', hacienda.nombre)
        hacienda.tel_contacto = data.get('tel_contacto', hacienda.tel_contacto)
        hacienda.ubicacion = data.get('ubicacion', hacienda.ubicacion)
        hacienda.descripcion = data.get('descripcion', hacienda.descripcion)
        hacienda.id_departamento = data.get('id_departamento', hacienda.id_departamento)
        hacienda.id_municipio = data.get('id_municipio', hacienda.id_municipio)
        hacienda.id_usuario = data.get('id_usuario', hacienda.id_usuario)
        db.session.commit()
        flash('Hacienda actualizada exitosamente.', 'success')
        return redirect(url_for('hacienda.index'))
    return render_template('hacienda/update.html', hacienda=hacienda)


@hacienda_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    hacienda = Hacienda.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(hacienda)
        db.session.commit()
        flash('Hacienda eliminada exitosamente.', 'success')
        return redirect(url_for('hacienda.index'))
    return render_template('hacienda/delete.html', hacienda=hacienda)

@hacienda_bp.route('/', methods=['GET'])
@token_required
def get_haciendas():
    haciendas = Hacienda.query.all()
    return jsonify([{"id": h.id_hacienda, "nombre": h.nombre} for h in haciendas])

@hacienda_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_hacienda(id):
    hacienda = Hacienda.query.get_or_404(id)
    return jsonify({"id": hacienda.id_hacienda, "nombre": hacienda.nombre})