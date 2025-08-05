from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.nacimiento import Nacimiento
from app.models.animal import Animal
from app.utils.jwt_utils import token_required
from flask_login import login_required

nacimiento_bp = Blueprint('nacimiento', __name__)

# --------------------------
# API CRUD ROUTES
# --------------------------
@nacimiento_bp.route('/api', methods=['GET'])
@token_required
def get_nacimientos_api():
    nacimientos = Nacimiento.query.all()
    return jsonify([{
        "id_nacimiento": n.id_nacimiento,
        "id_cria": n.id_cria,
        "id_madre": n.id_madre,
        "id_padre": n.id_padre,
        "fecha_nacimiento": n.fecha_nacimiento.isoformat(),
        "peso_nacimiento": float(n.peso_nacimiento),
        "tipo_parto": n.tipo_parto,
        "complicaciones": n.complicaciones,
        "observaciones": n.observaciones
    } for n in nacimientos])

@nacimiento_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_nacimiento(id):
    nacimiento = Nacimiento.query.get_or_404(id)
    return jsonify({
        "id_nacimiento": nacimiento.id_nacimiento,
        "id_cria": nacimiento.id_cria,
        "id_madre": nacimiento.id_madre,
        "id_padre": nacimiento.id_padre,
        "fecha_nacimiento": nacimiento.fecha_nacimiento.isoformat(),
        "peso_nacimiento": float(nacimiento.peso_nacimiento),
        "tipo_parto": nacimiento.tipo_parto,
        "complicaciones": nacimiento.complicaciones,
        "observaciones": nacimiento.observaciones
    })

@nacimiento_bp.route('/api', methods=['POST'])
@token_required
def create_nacimiento():
    data = request.get_json()
    new_nacimiento = Nacimiento(
        id_cria=data.get('id_cria'),
        id_madre=data.get('id_madre'),
        id_padre=data.get('id_padre'),
        fecha_nacimiento=data.get('fecha_nacimiento'),
        peso_nacimiento=data.get('peso_nacimiento'),
        tipo_parto=data.get('tipo_parto'),
        complicaciones=data.get('complicaciones'),
        observaciones=data.get('observaciones')
    )
    db.session.add(new_nacimiento)
    db.session.commit()
    return jsonify({"message": "Nacimiento created", "id": new_nacimiento.id_nacimiento}), 201

@nacimiento_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_nacimiento(id):
    nacimiento = Nacimiento.query.get_or_404(id)
    data = request.get_json()
    nacimiento.id_cria = data.get('id_cria', nacimiento.id_cria)
    nacimiento.id_madre = data.get('id_madre', nacimiento.id_madre)
    nacimiento.id_padre = data.get('id_padre', nacimiento.id_padre)
    nacimiento.fecha_nacimiento = data.get('fecha_nacimiento', nacimiento.fecha_nacimiento)
    nacimiento.peso_nacimiento = data.get('peso_nacimiento', nacimiento.peso_nacimiento)
    nacimiento.tipo_parto = data.get('tipo_parto', nacimiento.tipo_parto)
    nacimiento.complicaciones = data.get('complicaciones', nacimiento.complicaciones)
    nacimiento.observaciones = data.get('observaciones', nacimiento.observaciones)
    db.session.commit()
    return jsonify({"message": "Nacimiento updated"})

@nacimiento_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_nacimiento(id):
    nacimiento = Nacimiento.query.get_or_404(id)
    db.session.delete(nacimiento)
    db.session.commit()
    return jsonify({"message": "Nacimiento deleted"})

# --------------------------
# HTML CRUD ROUTES
# --------------------------
@nacimiento_bp.route('/', methods=['GET'])
@login_required
def index_html():
    nacimientos = Nacimiento.query.all()
    animals_lookup = {a.id_animal: a for a in Animal.query.all()}
    return render_template('nacimiento/index.html', nacimientos=nacimientos, animals_lookup=animals_lookup)

@nacimiento_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_html():
    if request.method == 'POST':
        data = request.form
        nuevo = Nacimiento(
            id_cria=data.get('id_cria'),
            id_madre=data.get('id_madre'),
            id_padre=data.get('id_padre'),
            fecha_nacimiento=data.get('fecha_nacimiento'),
            peso_nacimiento=data.get('peso_nacimiento'),
            tipo_parto=data.get('tipo_parto'),
            complicaciones=data.get('complicaciones'),
            observaciones=data.get('observaciones')
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Registro de nacimiento creado.', 'success')
        return redirect(url_for('nacimiento.index_html'))
    animals = Animal.query.all()
    return render_template('nacimiento/create.html', animals=animals)

@nacimiento_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_html(id):
    nac = Nacimiento.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        nac.id_cria = data.get('id_cria', nac.id_cria)
        nac.id_madre = data.get('id_madre', nac.id_madre)
        nac.id_padre = data.get('id_padre', nac.id_padre)
        nac.fecha_nacimiento = data.get('fecha_nacimiento', nac.fecha_nacimiento)
        nac.peso_nacimiento = data.get('peso_nacimiento', nac.peso_nacimiento)
        nac.tipo_parto = data.get('tipo_parto', nac.tipo_parto)
        nac.complicaciones = data.get('complicaciones', nac.complicaciones)
        nac.observaciones = data.get('observaciones', nac.observaciones)
        db.session.commit()
        flash('Registro de nacimiento actualizado.', 'success')
        return redirect(url_for('nacimiento.index_html'))
    animals = Animal.query.all()
    return render_template('nacimiento/update.html', nac=nac, animals=animals)

@nacimiento_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_html(id):
    nac = Nacimiento.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(nac)
        db.session.commit()
        flash('Registro de nacimiento eliminado.', 'success')
        return redirect(url_for('nacimiento.index_html'))
    return render_template('nacimiento/delete.html', nac=nac)