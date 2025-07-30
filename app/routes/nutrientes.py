from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.nutrientes import Nutrientes
from app.utils.jwt_utils import token_required

nutrientes_bp = Blueprint('nutrientes', __name__)

@nutrientes_bp.route('/api', methods=['GET'])
@token_required
def get_nutrientes():
    nutrientes = Nutrientes.query.all()
    return jsonify([{
        "id_nutriente": n.id_nutriente,
        "nombre": n.nombre,
        "unidad": n.unidad
    } for n in nutrientes])

@nutrientes_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_nutriente(id):
    nutriente = Nutrientes.query.get_or_404(id)
    return jsonify({
        "id_nutriente": nutriente.id_nutriente,
        "nombre": nutriente.nombre,
        "unidad": nutriente.unidad
    })

@nutrientes_bp.route('/api', methods=['POST'])
@token_required
def create_nutriente():
    data = request.get_json()
    new_nutriente = Nutrientes(
        nombre=data.get('nombre'),
        unidad=data.get('unidad')
    )
    db.session.add(new_nutriente)
    db.session.commit()
    return jsonify({"message": "Nutriente created", "id": new_nutriente.id_nutriente}), 201

@nutrientes_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_nutriente(id):
    nutriente = Nutrientes.query.get_or_404(id)
    data = request.get_json()
    nutriente.nombre = data.get('nombre', nutriente.nombre)
    nutriente.unidad = data.get('unidad', nutriente.unidad)
    db.session.commit()
    return jsonify({"message": "Nutriente updated"})

@nutrientes_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_nutriente(id):
    nutriente = Nutrientes.query.get_or_404(id)
    db.session.delete(nutriente)
    db.session.commit()
    return jsonify({"message": "Nutriente deleted"})

# --------------------------
# HTML CRUD ROUTES
# --------------------------
@nutrientes_bp.route('/', methods=['GET'])
@login_required
def index():
    nutrientes = Nutrientes.query.all()
    return render_template('nutrientes/index.html', nutrientes=nutrientes)

@nutrientes_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        data = request.form
        nuevo = Nutrientes(nombre=data.get('nombre'), unidad=data.get('unidad'))
        db.session.add(nuevo)
        db.session.commit()
        flash('Nutriente creado exitosamente.', 'success')
        return redirect(url_for('nutrientes.index'))
    return render_template('nutrientes/create.html')

@nutrientes_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    n = Nutrientes.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        n.nombre = data.get('nombre', n.nombre)
        n.unidad = data.get('unidad', n.unidad)
        db.session.commit()
        flash('Nutriente actualizado exitosamente.', 'success')
        return redirect(url_for('nutrientes.index'))
    return render_template('nutrientes/update.html', n=n)

@nutrientes_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_html(id):
    n = Nutrientes.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(n)
        db.session.commit()
        flash('Nutriente eliminado exitosamente.', 'success')
        return redirect(url_for('nutrientes.index'))
    return render_template('nutrientes/delete.html', n=n)