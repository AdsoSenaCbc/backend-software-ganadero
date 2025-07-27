from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.ingrediente_materia_prima import IngredienteMateriaPrima
from app.models.ingrediente import Ingrediente
from app.models.materia_prima import MateriaPrima
from app.utils.jwt_utils import token_required

ingrediente_materia_prima_bp = Blueprint('ingrediente_materia_prima', __name__, url_prefix='/ingrediente_materia_prima')

@ingrediente_materia_prima_bp.route('/', methods=['GET'])
@token_required
def get_ingrediente_materia_primas():
    relaciones = IngredienteMateriaPrima.query.all()
    return jsonify([{
        "id_ingrediente": r.id_ingrediente,
        "id_materia": r.id_materia,
        "cantidad_kg": float(r.cantidad_kg)
    } for r in relaciones])

@ingrediente_materia_prima_bp.route('/<int:id_ingrediente>/<int:id_materia>', methods=['GET'])
@token_required
def get_ingrediente_materia_prima(id_ingrediente, id_materia):
    relacion = IngredienteMateriaPrima.query.get_or_404((id_ingrediente, id_materia))
    return jsonify({
        "id_ingrediente": relacion.id_ingrediente,
        "id_materia": relacion.id_materia,
        "cantidad_kg": float(relacion.cantidad_kg)
    })

@ingrediente_materia_prima_bp.route('/', methods=['POST'])
@token_required
def create_ingrediente_materia_prima():
    data = request.get_json()
    new_relacion = IngredienteMateriaPrima(
        id_ingrediente=data.get('id_ingrediente'),
        id_materia=data.get('id_materia'),
        cantidad_kg=data.get('cantidad_kg')
    )
    db.session.add(new_relacion)
    db.session.commit()
    return jsonify({"message": "Ingrediente materia prima created", "id_ingrediente": new_relacion.id_ingrediente, "id_materia": new_relacion.id_materia}), 201

@ingrediente_materia_prima_bp.route('/<int:id_ingrediente>/<int:id_materia>', methods=['PUT'])
@token_required
def update_ingrediente_materia_prima(id_ingrediente, id_materia):
    relacion = IngredienteMateriaPrima.query.get_or_404((id_ingrediente, id_materia))
    data = request.get_json()
    relacion.cantidad_kg = data.get('cantidad_kg', relacion.cantidad_kg)
    db.session.commit()
    return jsonify({"message": "Ingrediente materia prima updated"})

@ingrediente_materia_prima_bp.route('/<int:id_ingrediente>/<int:id_materia>', methods=['DELETE'])
@token_required
def delete_ingrediente_materia_prima(id_ingrediente, id_materia):
    relacion = IngredienteMateriaPrima.query.get_or_404((id_ingrediente, id_materia))
    db.session.delete(relacion)
    db.session.commit()
    return jsonify({"message": "Ingrediente materia prima deleted"})

# Rutas Web
@ingrediente_materia_prima_bp.route('/web', methods=['GET'])
@login_required
def index():
    relaciones = db.session.query(
        IngredienteMateriaPrima,
        Ingrediente.nombre.label('nombre_ingrediente'),
        MateriaPrima.nombre.label('nombre_materia')
    ).join(
        Ingrediente, IngredienteMateriaPrima.id_ingrediente == Ingrediente.id_ingrediente
    ).join(
        MateriaPrima, IngredienteMateriaPrima.id_materia == MateriaPrima.id_materia
    ).all()
    return render_template('ingrediente_materia_prima/index.html', relaciones=relaciones)

@ingrediente_materia_prima_bp.route('/web/create', methods=['GET'])
@login_required
def create():
    ingredientes = Ingrediente.query.all()
    materias_primas = MateriaPrima.query.all()
    return render_template('ingrediente_materia_prima/create.html', 
                         ingredientes=ingredientes, 
                         materias_primas=materias_primas)

@ingrediente_materia_prima_bp.route('/web/create', methods=['POST'])
@login_required
def create_post():
    try:
        id_ingrediente = request.form.get('id_ingrediente')
        id_materia = request.form.get('id_materia')
        cantidad_kg = request.form.get('cantidad_kg', 0.0)
        
        if not id_ingrediente or not id_materia:
            flash('Debe seleccionar un ingrediente y una materia prima', 'error')
            return redirect(url_for('ingrediente_materia_prima.create'))
            
        # Verificar si ya existe la relación
        if IngredienteMateriaPrima.query.get((id_ingrediente, id_materia)):
            flash('Esta relación ya existe', 'error')
            return redirect(url_for('ingrediente_materia_prima.create'))
            
        nueva_relacion = IngredienteMateriaPrima(
            id_ingrediente=id_ingrediente,
            id_materia=id_materia,
            cantidad_kg=cantidad_kg
        )
        
        db.session.add(nueva_relacion)
        db.session.commit()
        flash('Relación creada exitosamente', 'success')
        return redirect(url_for('ingrediente_materia_prima.index'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear la relación: {str(e)}', 'error')
        return redirect(url_for('ingrediente_materia_prima.create'))

@ingrediente_materia_prima_bp.route('/web/<int:id_ingrediente>/<int:id_materia>/edit', methods=['GET'])
@login_required
def edit(id_ingrediente, id_materia):
    relacion = IngredienteMateriaPrima.query.get_or_404((id_ingrediente, id_materia))
    ingredientes = Ingrediente.query.all()
    materias_primas = MateriaPrima.query.all()
    
    return render_template('ingrediente_materia_prima/update.html', 
                         relacion=relacion,
                         ingredientes=ingredientes,
                         materias_primas=materias_primas)

@ingrediente_materia_prima_bp.route('/web/<int:id_ingrediente>/<int:id_materia>/edit', methods=['POST'])
@login_required
def update(id_ingrediente, id_materia):
    try:
        relacion = IngredienteMateriaPrima.query.get_or_404((id_ingrediente, id_materia))
        cantidad_kg = request.form.get('cantidad_kg', 0.0)
        
        relacion.cantidad_kg = cantidad_kg
        
        db.session.commit()
        flash('Relación actualizada exitosamente', 'success')
        return redirect(url_for('ingrediente_materia_prima.index'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar la relación: {str(e)}', 'error')
        return redirect(url_for('ingrediente_materia_prima.edit', 
                              id_ingrediente=id_ingrediente, 
                              id_materia=id_materia))

@ingrediente_materia_prima_bp.route('/web/<int:id_ingrediente>/<int:id_materia>/delete', methods=['GET'])
@login_required
def delete_web(id_ingrediente, id_materia):
    try:
        relacion = IngredienteMateriaPrima.query.get_or_404((id_ingrediente, id_materia))
        db.session.delete(relacion)
        db.session.commit()
        flash('Relación eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la relación: {str(e)}', 'error')
    return redirect(url_for('ingrediente_materia_prima.index'))