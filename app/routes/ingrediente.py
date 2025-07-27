from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.ingrediente import Ingrediente
from app.utils.jwt_utils import token_required

ingrediente_bp = Blueprint('ingrediente', __name__, url_prefix='/ingrediente')

@ingrediente_bp.route('/', methods=['GET'])
@token_required
def get_ingredientes():
    ingredientes = Ingrediente.query.all()
    return jsonify([{
        "id_ingrediente": i.id_ingrediente,
        "nombre": i.nombre,
        "tipo": i.tipo,
        "descripcion": i.descripcion,
        "costo_kg": float(i.costo_kg)
    } for i in ingredientes])

@ingrediente_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_ingrediente(id):
    ingrediente = Ingrediente.query.get_or_404(id)
    return jsonify({
        "id_ingrediente": ingrediente.id_ingrediente,
        "nombre": ingrediente.nombre,
        "tipo": ingrediente.tipo,
        "descripcion": ingrediente.descripcion,
        "costo_kg": float(ingrediente.costo_kg)
    })

@ingrediente_bp.route('/', methods=['POST'])
@token_required
def create_ingrediente():
    data = request.get_json()
    new_ingrediente = Ingrediente(
        nombre=data.get('nombre'),
        tipo=data.get('tipo'),
        descripcion=data.get('descripcion'),
        costo_kg=data.get('costo_kg')
    )
    db.session.add(new_ingrediente)
    db.session.commit()
    return jsonify({"message": "Ingrediente created", "id": new_ingrediente.id_ingrediente}), 201

@ingrediente_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_ingrediente(id):
    ingrediente = Ingrediente.query.get_or_404(id)
    data = request.get_json()
    ingrediente.nombre = data.get('nombre', ingrediente.nombre)
    ingrediente.tipo = data.get('tipo', ingrediente.tipo)
    ingrediente.descripcion = data.get('descripcion', ingrediente.descripcion)
    ingrediente.costo_kg = data.get('costo_kg', ingrediente.costo_kg)
    db.session.commit()
    return jsonify({"message": "Ingrediente updated"})

@ingrediente_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_ingrediente(id):
    ingrediente = Ingrediente.query.get_or_404(id)
    db.session.delete(ingrediente)
    db.session.commit()
    return jsonify({"message": "Ingrediente deleted"})

# Rutas Web
@ingrediente_bp.route('/web', methods=['GET'])
@login_required
def index():
    ingredientes = Ingrediente.query.all()
    return render_template('ingrediente/index.html', ingredientes=ingredientes)

@ingrediente_bp.route('/web/create', methods=['GET'])
@login_required
def create():
    return render_template('ingrediente/create.html')

@ingrediente_bp.route('/web/create', methods=['POST'])
@login_required
def create_post():
    try:
        nombre = request.form.get('nombre')
        tipo = request.form.get('tipo', '')
        descripcion = request.form.get('descripcion', '')
        costo_kg = request.form.get('costo_kg', 0.0)
        
        if not nombre:
            flash('El nombre es obligatorio', 'error')
            return redirect(url_for('ingrediente.create'))
            
        nuevo_ingrediente = Ingrediente(
            nombre=nombre,
            tipo=tipo,
            descripcion=descripcion,
            costo_kg=costo_kg
        )
        
        db.session.add(nuevo_ingrediente)
        db.session.commit()
        flash('Ingrediente creado exitosamente', 'success')
        return redirect(url_for('ingrediente.index'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear el ingrediente: {str(e)}', 'error')
        return redirect(url_for('ingrediente.create'))

@ingrediente_bp.route('/web/<int:id>/edit', methods=['GET'])
@login_required
def edit(id):
    ingrediente = Ingrediente.query.get_or_404(id)
    return render_template('ingrediente/update.html', ingrediente=ingrediente)

@ingrediente_bp.route('/web/<int:id>/edit', methods=['POST'])
@login_required
def update(id):
    try:
        ingrediente = Ingrediente.query.get_or_404(id)
        
        nombre = request.form.get('nombre')
        tipo = request.form.get('tipo', '')
        descripcion = request.form.get('descripcion', '')
        costo_kg = request.form.get('costo_kg', 0.0)
        
        if not nombre:
            flash('El nombre es obligatorio', 'error')
            return redirect(url_for('ingrediente.edit', id=id))
            
        ingrediente.nombre = nombre
        ingrediente.tipo = tipo
        ingrediente.descripcion = descripcion
        ingrediente.costo_kg = costo_kg
        
        db.session.commit()
        flash('Ingrediente actualizado exitosamente', 'success')
        return redirect(url_for('ingrediente.index'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar el ingrediente: {str(e)}', 'error')
        return redirect(url_for('ingrediente.edit', id=id))

@ingrediente_bp.route('/web/<int:id>/delete', methods=['GET'])
@login_required
def delete_web(id):
    try:
        ingrediente = Ingrediente.query.get_or_404(id)
        db.session.delete(ingrediente)
        db.session.commit()
        flash('Ingrediente eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el ingrediente: {str(e)}', 'error')
    return redirect(url_for('ingrediente.index'))