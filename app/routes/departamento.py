from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.departamento import Departamento
from app.utils.jwt_utils import token_required
from flask_login import login_required

departamento_bp = Blueprint('departamento', __name__)

# --------------------------
# API JSON ENDPOINTS
# Ruta pública con prefijo /api/departamentos/
# Ruta API pública: /departamento/api/departamentos/
@departamento_bp.route('/', methods=['GET'])
@token_required
def list_departamentos_public():
    return get_departamentos_api()

# Endpoint específico para el frontend React
@departamento_bp.route('/list', methods=['GET'])
@token_required
def api_list_departamentos():
    return get_departamentos_api()

# --------------------------
@departamento_bp.route('/api', methods=['GET'])
@token_required
def get_departamentos_api():
    departamentos = Departamento.query.all()
    return jsonify([
        {
            "id_departamento": d.id_departamento,
            "nombre_departamento": d.nombre_departamento
        } for d in departamentos
    ])

@departamento_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_departamento_api(id):
    departamento = Departamento.query.get_or_404(id)
    return jsonify({
        "id_departamento": departamento.id_departamento,
        "nombre_departamento": departamento.nombre_departamento
    })

@departamento_bp.route('/', methods=['GET'])
@login_required
def index():
    departamentos = Departamento.query.all()
    return render_template('departamento/index.html', departamentos=departamentos)

# --------------------------
# FORM-BASED CRUD ENDPOINTS
# --------------------------
@departamento_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_departamento():
    if request.method == 'POST':
        nombre = request.form.get('nombre_departamento')
        if not nombre:
            flash('El nombre es requerido', 'danger')
            return redirect(url_for('departamento.create_departamento'))
        new_departamento = Departamento(nombre_departamento=nombre)
        db.session.add(new_departamento)
        db.session.commit()
        flash('Departamento creado exitosamente.', 'success')
        return redirect(url_for('departamento.index'))
    return render_template('departamento/create.html')

@departamento_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_departamento(id):
    departamento = Departamento.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre_departamento')
        departamento.nombre_departamento = nombre or departamento.nombre_departamento
        db.session.commit()
        flash('Departamento actualizado exitosamente.', 'success')
        return redirect(url_for('departamento.index'))
    return render_template('departamento/update.html', departamento=departamento)

@departamento_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_departamento(id):
    departamento = Departamento.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(departamento)
        db.session.commit()
        flash('Departamento eliminado exitosamente.', 'success')
        return redirect(url_for('departamento.index'))
    return render_template('departamento/delete.html', departamento=departamento)

# --------------------------
# API CRUD ENDPOINTS (token protected)
# --------------------------

@departamento_bp.route('/api', methods=['POST'])
@token_required
def create_departamento_api():
    data = request.get_json()
    new_departamento = Departamento(
        nombre_departamento=data.get('nombre_departamento')
    )
    db.session.add(new_departamento)
    db.session.commit()
    return jsonify({"message": "Departamento created", "id": new_departamento.id_departamento}), 201

@departamento_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_departamento_api(id):
    departamento = Departamento.query.get_or_404(id)
    data = request.get_json()
    departamento.nombre_departamento = data.get('nombre_departamento', departamento.nombre_departamento)
    db.session.commit()
    return jsonify({"message": "Departamento updated"})

@departamento_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_departamento_api(id):
    departamento = Departamento.query.get_or_404(id)
    db.session.delete(departamento)
    db.session.commit()
    return jsonify({"message": "Departamento deleted"})

