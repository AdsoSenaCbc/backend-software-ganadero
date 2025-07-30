from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.raza import Raza
from app.utils.jwt_utils import token_required
from flask_login import login_required

raza_bp = Blueprint('raza', __name__)

# --------------------------
# HTML FORM ROUTES
# --------------------------
@raza_bp.route('/', methods=['GET'])
@login_required
def index():
    razas = Raza.query.all()
    return render_template('raza/index.html', razas=razas)

@raza_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_raza_form():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if not nombre:
            flash('El nombre es obligatorio', 'danger')
            return redirect(url_for('raza.create_raza_form'))
        nueva = Raza(nombre=nombre)
        db.session.add(nueva)
        db.session.commit()
        flash('Raza creada correctamente.', 'success')
        return redirect(url_for('raza.index'))
    return render_template('raza/create.html')

@raza_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_raza_form(id):
    raza = Raza.query.get_or_404(id)
    if request.method == 'POST':
        raza.nombre = request.form.get('nombre', raza.nombre)
        db.session.commit()
        flash('Raza actualizada correctamente.', 'success')
        return redirect(url_for('raza.index'))
    return render_template('raza/update.html', raza=raza)

@raza_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_raza_form(id):
    raza = Raza.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(raza)
        db.session.commit()
        flash('Raza eliminada correctamente.', 'success')
        return redirect(url_for('raza.index'))
    return render_template('raza/delete.html', raza=raza)

# --------------------------
# API JSON ENDPOINTS
# --------------------------
@raza_bp.route('/api/razas', methods=['GET'])
@token_required
def get_razas_api():
    razas = Raza.query.all()
    return jsonify([{
        "id_raza": r.id_raza,
        "nombre": r.nombre
    } for r in razas])

@raza_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_raza_api(id):
    raza = Raza.query.get_or_404(id)
    r = Raza.query.get_or_404(id)
    return jsonify({
        "id_raza": r.id_raza,
        "nombre": r.nombre
    })

@raza_bp.route('/api/razas', methods=['POST'])
@token_required
def create_raza_api():
    data = request.get_json()
    new_raza = Raza(
        nombre=data.get('nombre')
    )
    db.session.add(new_raza)
    db.session.commit()
    return jsonify({"message": "Raza created", "id": new_raza.id_raza}), 201

@raza_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_raza_api(id):
    raza = Raza.query.get_or_404(id)
    data = request.get_json()
    raza.nombre = data.get('nombre', raza.nombre)
    db.session.commit()
    return jsonify({"message": "Raza updated"})

@raza_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_raza_api(id):
    raza = Raza.query.get_or_404(id)
    db.session.delete(raza)
    db.session.commit()
    return jsonify({"message": "Raza deleted"})

# --------------------------
# WEB ROUTES
# --------------------------
@raza_bp.route('/', methods=['GET'])
@login_required
def index():
    razas = Raza.query.all()
    return render_template('raza/index.html', razas=razas)

@raza_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        data = request.form
        new_raza = Raza(
            id_raza=data.get('id_raza'),
            nombre=data.get('nombre')
        )
        db.session.add(new_raza)
        db.session.commit()
        flash('Raza creada exitosamente.', 'success')
        return redirect(url_for('raza.index'))
    return render_template('raza/create.html')

@raza_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    raza = Raza.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        raza.id_raza = data.get('id_raza', raza.id_raza)
        raza.nombre = data.get('nombre', raza.nombre)
        db.session.commit()
        flash('Raza actualizada exitosamente.', 'success')
        return redirect(url_for('raza.index'))
    return render_template('raza/update.html', raza=raza)

@raza_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    raza = Raza.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(raza)
        db.session.commit()
        flash('Raza eliminada exitosamente.', 'success')
        return redirect(url_for('raza.index'))
    return render_template('raza/delete.html', raza=raza)