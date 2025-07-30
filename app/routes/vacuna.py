from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.vacuna import Vacuna
from app.utils.jwt_utils import token_required
from flask_login import login_required

vacuna_bp = Blueprint('vacuna', __name__)

# --------------------------
# HTML FORM ROUTES
# --------------------------
@vacuna_bp.route('/', methods=['GET'])
@login_required
def index():
    vacunas = Vacuna.query.all()
    return render_template('vacuna/index.html', vacunas=vacunas)

@vacuna_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_vacuna_form():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        if not nombre:
            flash('El nombre es obligatorio', 'danger')
            return redirect(url_for('vacuna.create_vacuna_form'))
        nueva = Vacuna(nombre=nombre, descripcion=descripcion)
        db.session.add(nueva)
        db.session.commit()
        flash('Vacuna creada correctamente.', 'success')
        return redirect(url_for('vacuna.index'))
    return render_template('vacuna/create.html')

@vacuna_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_vacuna_form(id):
    vacuna = Vacuna.query.get_or_404(id)
    if request.method == 'POST':
        vacuna.nombre = request.form.get('nombre', vacuna.nombre)
        vacuna.descripcion = request.form.get('descripcion', vacuna.descripcion)
        db.session.commit()
        flash('Vacuna actualizada correctamente.', 'success')
        return redirect(url_for('vacuna.index'))
    return render_template('vacuna/update.html', vacuna=vacuna)

@vacuna_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_vacuna_form(id):
    vacuna = Vacuna.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(vacuna)
        db.session.commit()
        flash('Vacuna eliminada correctamente.', 'success')
        return redirect(url_for('vacuna.index'))
    return render_template('vacuna/delete.html', vacuna=vacuna)

# --------------------------
# API JSON ENDPOINTS
# --------------------------

@vacuna_bp.route('/api/vacunas', methods=['GET'])
@token_required
def get_vacunas_api():
    vacunas = Vacuna.query.all()
    return jsonify([{
        "id_vacuna": v.id_vacuna,
        "nombre": v.nombre,
        "descripcion": v.descripcion
    } for v in vacunas])

@vacuna_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_vacuna_api(id):
    vacuna = Vacuna.query.get_or_404(id)
    return jsonify({
        "id_vacuna": vacuna.id_vacuna,
        "nombre": vacuna.nombre,
        "descripcion": vacuna.descripcion
    })

@vacuna_bp.route('/api/vacunas', methods=['POST'])
@token_required
def create_vacuna_api():
    data = request.get_json()
    new_vacuna = Vacuna(
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion')
    )
    db.session.add(new_vacuna)
    db.session.commit()
    return jsonify({"message": "Vacuna created", "id": new_vacuna.id_vacuna}), 201

@vacuna_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_vacuna_api(id):
    vacuna = Vacuna.query.get_or_404(id)
    data = request.get_json()
    vacuna.nombre = data.get('nombre', vacuna.nombre)
    vacuna.descripcion = data.get('descripcion', vacuna.descripcion)
    db.session.commit()
    return jsonify({"message": "Vacuna updated"})

@vacuna_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_vacuna_api(id):
    vacuna = Vacuna.query.get_or_404(id)
    db.session.delete(vacuna)
    db.session.commit()
    return jsonify({"message": "Vacuna deleted"})

# --------------------------
# WEB ROUTES
# --------------------------
@vacuna_bp.route('/', methods=['GET'])
@login_required
def index():
    vacunas = Vacuna.query.all()
    return render_template('vacuna/index.html', vacunas=vacunas)

@vacuna_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        data = request.form
        try:
            dosis = float(data.get('dosis_recomendada')) if data.get('dosis_recomendada') else None
            new_vacuna = Vacuna(
                nombre=data.get('nombre'),
                descripcion=data.get('descripcion'),
                dosis_recomendada=dosis
            )
            db.session.add(new_vacuna)
            db.session.commit()
            flash('Vacuna creada exitosamente.', 'success')
            return redirect(url_for('vacuna.index'))
        except ValueError:
            flash('Error: La dosis debe ser un número válido.', 'error')
    return render_template('vacuna/create.html')

@vacuna_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    vacuna = Vacuna.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        try:
            dosis = float(data.get('dosis_recomendada')) if data.get('dosis_recomendada') else None
            vacuna.nombre = data.get('nombre', vacuna.nombre)
            vacuna.descripcion = data.get('descripcion', vacuna.descripcion)
            vacuna.dosis_recomendada = dosis
            db.session.commit()
            flash('Vacuna actualizada exitosamente.', 'success')
            return redirect(url_for('vacuna.index'))
        except ValueError:
            flash('Error: La dosis debe ser un número válido.', 'error')
    return render_template('vacuna/update.html', vacuna=vacuna)

@vacuna_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    vacuna = Vacuna.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(vacuna)
        db.session.commit()
        flash('Vacuna eliminada exitosamente.', 'success')
        return redirect(url_for('vacuna.index'))
    return render_template('vacuna/delete.html', vacuna=vacuna)