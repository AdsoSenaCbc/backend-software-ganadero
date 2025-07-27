from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.nutrientes import Nutrientes
from app.utils.jwt_utils import token_required

nutrientes_bp = Blueprint('nutrientes', __name__, url_prefix='/nutrientes')

@nutrientes_bp.route('/', methods=['GET'])
@token_required
def get_nutrientes():
    nutrientes = Nutrientes.query.all()
    return jsonify([{
        "id_nutriente": n.id_nutriente,
        "nombre": n.nombre,
        "unidad": n.unidad
    } for n in nutrientes])

@nutrientes_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_nutriente(id):
    nutriente = Nutrientes.query.get_or_404(id)
    return jsonify({
        "id_nutriente": nutriente.id_nutriente,
        "nombre": nutriente.nombre,
        "unidad": nutriente.unidad
    })

@nutrientes_bp.route('/', methods=['POST'])
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

@nutrientes_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_nutriente(id):
    nutriente = Nutrientes.query.get_or_404(id)
    data = request.get_json()
    nutriente.nombre = data.get('nombre', nutriente.nombre)
    nutriente.unidad = data.get('unidad', nutriente.unidad)
    db.session.commit()
    return jsonify({"message": "Nutriente updated"})

@nutrientes_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_nutriente(id):
    nutriente = Nutrientes.query.get_or_404(id)
    db.session.delete(nutriente)
    db.session.commit()
    return jsonify({"message": "Nutriente deleted"})

# Web Routes
@nutrientes_bp.route('/web', methods=['GET'])
@login_required
def index():
    nutrientes = Nutrientes.query.all()
    return render_template('nutrientes/index.html', nutrientes=nutrientes)

@nutrientes_bp.route('/web/create', methods=['GET'])
@login_required
def create():
    return render_template('nutrientes/create.html')

@nutrientes_bp.route('/web/create', methods=['POST'])
@login_required
def create_post():
    try:
        nombre = request.form.get('nombre')
        unidad = request.form.get('unidad')
        
        if not nombre:
            flash('El campo nombre es obligatorio', 'error')
            return redirect(url_for('nutrientes.create'))
            
        # Verificar si ya existe un nutriente con el mismo nombre
        if Nutrientes.query.filter_by(nombre=nombre).first():
            flash('Ya existe un nutriente con este nombre', 'error')
            return redirect(url_for('nutrientes.create'))
            
        nuevo_nutriente = Nutrientes(
            nombre=nombre,
            unidad=unidad
        )
        
        db.session.add(nuevo_nutriente)
        db.session.commit()
        flash('Nutriente creado exitosamente', 'success')
        return redirect(url_for('nutrientes.index'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear el nutriente: {str(e)}', 'error')
        return redirect(url_for('nutrientes.create'))

@nutrientes_bp.route('/web/<int:id>/edit', methods=['GET'])
@login_required
def edit(id):
    nutriente = Nutrientes.query.get_or_404(id)
    return render_template('nutrientes/update.html', nutriente=nutriente)

@nutrientes_bp.route('/web/<int:id>/edit', methods=['POST'])
@login_required
def update(id):
    try:
        nutriente = Nutrientes.query.get_or_404(id)
        nombre = request.form.get('nombre')
        unidad = request.form.get('unidad')
        
        if not nombre:
            flash('El campo nombre es obligatorio', 'error')
            return redirect(url_for('nutrientes.edit', id=id))
            
        # Verificar si ya existe otro nutriente con el mismo nombre
        existing = Nutrientes.query.filter(Nutrientes.nombre == nombre, Nutrientes.id_nutriente != id).first()
        if existing:
            flash('Ya existe otro nutriente con este nombre', 'error')
            return redirect(url_for('nutrientes.edit', id=id))
            
        nutriente.nombre = nombre
        nutriente.unidad = unidad
        
        db.session.commit()
        flash('Nutriente actualizado exitosamente', 'success')
        return redirect(url_for('nutrientes.index'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar el nutriente: {str(e)}', 'error')
        return redirect(url_for('nutrientes.edit', id=id))

@nutrientes_bp.route('/web/<int:id>/delete', methods=['GET'])
@login_required
def delete_web(id):
    try:
        nutriente = Nutrientes.query.get_or_404(id)
        db.session.delete(nutriente)
        db.session.commit()
        flash('Nutriente eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el nutriente: {str(e)}', 'error')
    return redirect(url_for('nutrientes.index'))