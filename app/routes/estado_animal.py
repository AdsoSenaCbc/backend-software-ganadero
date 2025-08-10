from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.estado_animal import EstadoAnimal
from app.utils.jwt_utils import token_required
from flask_login import login_required

estado_animal_bp = Blueprint('estado_animal', __name__)

# --------------------------
# HTML FORM ROUTES
# --------------------------
@estado_animal_bp.route('/', methods=['GET'])
@login_required
def index():
    estados = EstadoAnimal.query.all()
    return render_template('estado_animal/index.html', estados=estados)

@estado_animal_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_estado():
    if request.method == 'POST':
        nombre = request.form.get('nombre_estado')
        if not nombre:
            flash('El nombre es requerido', 'danger')
            return redirect(url_for('estado_animal.create_estado'))
        nuevo = EstadoAnimal(nombre_estado=nombre)
        db.session.add(nuevo)
        db.session.commit()
        flash('Estado creado exitosamente.', 'success')
        return redirect(url_for('estado_animal.index'))
    return render_template('estado_animal/create.html')

@estado_animal_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_estado(id):
    estado = EstadoAnimal.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre_estado')
        estado.nombre_estado = nombre or estado.nombre_estado
        db.session.commit()
        flash('Estado actualizado exitosamente.', 'success')
        return redirect(url_for('estado_animal.index'))
    return render_template('estado_animal/update.html', estado=estado)

@estado_animal_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_estado(id):
    estado = EstadoAnimal.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(estado)
        db.session.commit()
        flash('Estado eliminado exitosamente.', 'success')
        return redirect(url_for('estado_animal.index'))
    return render_template('estado_animal/delete.html', estado=estado)

# --------------------------
# API JSON ENDPOINTS
# --------------------------

@estado_animal_bp.route('/', methods=['GET'])
@token_required
def get_estados_api():
    estados = EstadoAnimal.query.all()
    return jsonify([{
        "id_estado": e.id_estado,
        "nombre_estado": e.nombre_estado
    } for e in estados])

@estado_animal_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_estado_api(id):
    estado = EstadoAnimal.query.get_or_404(id)
    return jsonify({
        "id_estado": estado.id_estado,
        "nombre_estado": estado.nombre_estado
    })

@estado_animal_bp.route('/', methods=['POST'])
@token_required
def create_estado_api():
    data = request.get_json()
    new_estado = EstadoAnimal(
        nombre_estado=data.get('nombre_estado')
    )
    db.session.add(new_estado)
    db.session.commit()
    return jsonify({"message": "Estado animal created", "id": new_estado.id_estado}), 201

@estado_animal_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_estado_api(id):
    estado = EstadoAnimal.query.get_or_404(id)
    data = request.get_json()
    estado.nombre_estado = data.get('nombre_estado', estado.nombre_estado)
    db.session.commit()
    return jsonify({"message": "Estado animal updated"})

@estado_animal_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_estado_api(id):
    estado = EstadoAnimal.query.get_or_404(id)
    db.session.delete(estado)
    db.session.commit()
    return jsonify({"message": "Estado animal deleted"})

# --------------------------
# Alias lista para frontend
# --------------------------
@estado_animal_bp.route('/list', methods=['GET'])
@token_required
def list_estados_api():
    """Devuelve los estados animales (alias)."""
    return get_estados_api()