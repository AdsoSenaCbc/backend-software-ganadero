from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.hacienda import Hacienda
from app.utils.jwt_utils import token_required

hacienda_bp = Blueprint('hacienda', __name__)

# --------------------------
# API JSON ENDPOINTS
# --------------------------

# API: Lista de haciendas
@hacienda_bp.route('/', methods=['GET'])
@token_required
def get_haciendas_api():
    """Retorna la lista de haciendas en formato JSON"""
    haciendas = Hacienda.query.all()
    return jsonify([{"id": h.id_hacienda, "nombre": h.nombre} for h in haciendas])

@hacienda_bp.route('/', methods=['POST'])
@token_required
def create_hacienda_api():
    """Crea una nueva hacienda a partir de JSON"""
    data = request.get_json()
    if not data or 'nombre' not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    nueva = Hacienda(
        nombre=data.get('nombre'),
        tel_contacto=data.get('tel_contacto'),
        ubicacion=data.get('ubicacion'),
        descripcion=data.get('descripcion'),
        id_departamento=data.get('id_departamento'),
        id_municipio=data.get('id_municipio'),
        id_usuario=data.get('id_usuario'),
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({"message": "Hacienda creada", "id": nueva.id_hacienda}), 201

# Alias lista para selects
@hacienda_bp.route('/list', methods=['GET'])
@token_required
def list_haciendas_api():
    return get_haciendas_api()

@hacienda_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_hacienda_api(id):
    """Elimina una hacienda"""
    hacienda = Hacienda.query.get_or_404(id)
    db.session.delete(hacienda)
    db.session.commit()
    return jsonify({"message": "Hacienda eliminada"}), 200

@hacienda_bp.route('/<int:id>', methods=['GET'])
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
        
    # GET: cargar listas para selects
    from app.models.departamento import Departamento
    from app.models.municipio import Municipio
    from app.models.usuario import Usuario
    departamentos = Departamento.query.all()
    municipios = Municipio.query.all()
    usuarios = Usuario.query.all()
    return render_template('hacienda/create.html', departamentos=departamentos, municipios=municipios, usuarios=usuarios)


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
    # GET: cargar selects
    from app.models.departamento import Departamento
    from app.models.municipio import Municipio
    from app.models.usuario import Usuario
    departamentos = Departamento.query.all()
    municipios = Municipio.query.all()
    usuarios = Usuario.query.all()
    return render_template('hacienda/update.html', hacienda=hacienda, departamentos=departamentos, municipios=municipios, usuarios=usuarios)


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