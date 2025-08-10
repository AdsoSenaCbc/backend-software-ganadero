from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.especie import Especie
from app.utils.jwt_utils import token_required
from flask_login import login_required

especie_bp = Blueprint('especie', __name__)

# --------------------------
# HTML FORM ROUTES
# --------------------------
@especie_bp.route('/', methods=['GET'])
@login_required
def index():
    especies = Especie.query.all()
    return render_template('especie/index.html', especies=especies)

@especie_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_especie_form():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if not nombre:
            flash('El nombre es obligatorio', 'danger')
            return redirect(url_for('especie.create_especie_form'))
        nueva = Especie(nombre=nombre)
        db.session.add(nueva)
        db.session.commit()
        flash('Especie creada correctamente.', 'success')
        return redirect(url_for('especie.index'))
    return render_template('especie/create.html')

@especie_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_especie_form(id):
    especie = Especie.query.get_or_404(id)
    if request.method == 'POST':
        especie.nombre = request.form.get('nombre', especie.nombre)
        db.session.commit()
        flash('Especie actualizada correctamente.', 'success')
        return redirect(url_for('especie.index'))
    return render_template('especie/update.html', especie=especie)

@especie_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_especie_form(id):
    especie = Especie.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(especie)
        db.session.commit()
        flash('Especie eliminada correctamente.', 'success')
        return redirect(url_for('especie.index'))
    return render_template('especie/delete.html', especie=especie)

# --------------------------
# API JSON ENDPOINTS
# --------------------------
@especie_bp.route('/', methods=['GET'])
@token_required
def get_especies_api():
    especies = Especie.query.all()
    return jsonify([{
        "id_especie": e.id_especie,
        "nombre": e.nombre
    } for e in especies])

# Alias lista para frontend
@especie_bp.route('/list', methods=['GET'])
@token_required
def list_especies_api():
    """Devuelve todas las especies (alias)."""
    return get_especies_api()

@especie_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_especie_api(id):
    especie = Especie.query.get_or_404(id)
    return jsonify({
        "id_especie": e.id_especie,
        "nombre": e.nombre
    })

@especie_bp.route('/', methods=['POST'])
@token_required
def create_especie_api():
    data = request.get_json()
    new_especie = Especie(
        nombre=data.get('nombre')
    )
    db.session.add(new_especie)
    db.session.commit()
    return jsonify({"message": "Especie created", "id": new_especie.id_especie}), 201

@especie_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_especie_api(id):
    especie = Especie.query.get_or_404(id)
    data = request.get_json()
    especie.nombre = data.get('nombre', especie.nombre)
    db.session.commit()
    return jsonify({"message": "Especie updated"})

@especie_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_especie_api(id):

    especie = Especie.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        especie.id_especie = data.get('id_especie', especie.id_especie)
        especie.nombre = data.get('nombre', especie.nombre)
        db.session.commit()
        flash('Especie actualizada exitosamente.', 'success')
        return redirect(url_for('especie.index'))
    return render_template('especie/update.html', especie=especie)

@especie_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    especie = Especie.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(especie)
        db.session.commit()
        flash('Especie eliminada exitosamente.', 'success')
        return redirect(url_for('especie.index'))
    return render_template('especie/delete.html', especie=especie)