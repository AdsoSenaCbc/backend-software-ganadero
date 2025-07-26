from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.especie import Especie
from app.utils.jwt_utils import token_required

especie_bp = Blueprint('especie', __name__)

# --------------------------
# API JSON ENDPOINTS
# --------------------------
@especie_bp.route('/api', methods=['GET'])
@token_required
def get_especies_api():
    especies = Especie.query.all()
    return jsonify([{
        "id_especie": e.id_especie,
        "nombre": e.nombre
    } for e in especies])

@especie_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_especie_api(id):
    e = Especie.query.get_or_404(id)
    return jsonify({
        "id_especie": e.id_especie,
        "nombre": e.nombre
    })

# --------------------------
# WEB ROUTES
# --------------------------
@especie_bp.route('/', methods=['GET'])
@login_required
def index():
    especies = Especie.query.all()
    return render_template('especie/index.html', especies=especies)

@especie_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        data = request.form
        new_especie = Especie(
            id_especie=data.get('id_especie'),
            nombre=data.get('nombre')
        )
        db.session.add(new_especie)
        db.session.commit()
        flash('Especie creada exitosamente.', 'success')
        return redirect(url_for('especie.index'))
    return render_template('especie/create.html')

@especie_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
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