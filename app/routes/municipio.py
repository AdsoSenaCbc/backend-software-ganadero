from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.municipio import Municipio
from app.utils.jwt_utils import token_required
from flask_login import login_required

municipio_bp = Blueprint('municipio', __name__)

# --------------------------
# HTML FORM ROUTES
# --------------------------
@municipio_bp.route('/', methods=['GET'])
@login_required
def index():
    municipios = Municipio.query.all()
    return render_template('municipio/index.html', municipios=municipios)

@municipio_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_municipio():
    if request.method == 'POST':
        nombre = request.form.get('nombre_municipio')
        id_dep = request.form.get('id_departamento')
        if not nombre:
            flash('El nombre es requerido', 'danger')
            return redirect(url_for('municipio.create_municipio'))
        new_mun = Municipio(nombre_municipio=nombre, id_departamento=id_dep)
        db.session.add(new_mun)
        db.session.commit()
        flash('Municipio creado exitosamente.', 'success')
        return redirect(url_for('municipio.index'))
    return render_template('municipio/create.html')

@municipio_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_municipio(id):
    municipio = Municipio.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre_municipio')
        id_dep = request.form.get('id_departamento')
        municipio.nombre_municipio = nombre or municipio.nombre_municipio
        municipio.id_departamento = id_dep or municipio.id_departamento
        db.session.commit()
        flash('Municipio actualizado exitosamente.', 'success')
        return redirect(url_for('municipio.index'))
    return render_template('municipio/update.html', municipio=municipio)

@municipio_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_municipio(id):
    municipio = Municipio.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(municipio)
        db.session.commit()
        flash('Municipio eliminado exitosamente.', 'success')
        return redirect(url_for('municipio.index'))
    return render_template('municipio/delete.html', municipio=municipio)


# --------------------------
# API JSON ENDPOINTS
# Ruta pública con prefijo /api/municipios/
@municipio_bp.route('/', methods=['GET'])
@token_required
def list_municipios_public():
    return get_municipios_api()

# Endpoint específico para el frontend React
@municipio_bp.route('/list', methods=['GET'])
@token_required
def api_list_municipios():
    return get_municipios_api()

# --------------------------
@municipio_bp.route('/api', methods=['GET'])
@token_required
def get_municipios_api():
    municipios = Municipio.query.all()
    return jsonify([{
        "id_municipio": m.id_municipio,
        "nombre_municipio": m.nombre_municipio,
        "id_departamento": m.id_departamento
    } for m in municipios])

@municipio_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_municipio_api(id):
    municipio = Municipio.query.get_or_404(id)
    return jsonify({
        "id_municipio": municipio.id_municipio,
        "nombre_municipio": municipio.nombre_municipio,
        "id_departamento": municipio.id_departamento
    })

@municipio_bp.route('/api', methods=['POST'])
@token_required
def create_municipio_api():
    data = request.get_json()
    new_municipio = Municipio(
        nombre_municipio=data.get('nombre_municipio'),
        id_departamento=data.get('id_departamento')
    )
    db.session.add(new_municipio)
    db.session.commit()
    return jsonify({"message": "Municipio created", "id": new_municipio.id_municipio}), 201

@municipio_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_municipio_api(id):
    municipio = Municipio.query.get_or_404(id)
    data = request.get_json()
    municipio.nombre_municipio = data.get('nombre_municipio', municipio.nombre_municipio)
    municipio.id_departamento = data.get('id_departamento', municipio.id_departamento)
    db.session.commit()
    return jsonify({"message": "Municipio updated"})

@municipio_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_municipio_api(id):
    municipio = Municipio.query.get_or_404(id)
    db.session.delete(municipio)
    db.session.commit()
    return jsonify({"message": "Municipio deleted"})