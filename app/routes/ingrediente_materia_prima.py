from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.ingrediente_materia_prima import IngredienteMateriaPrima
from app.models.ingrediente import Ingrediente
from app.models.materia_prima import MateriaPrima
from app.utils.jwt_utils import token_required

ingrediente_materia_prima_bp = Blueprint('ingrediente_materia_prima', __name__, url_prefix='/ingrediente_materia_prima')

@ingrediente_materia_prima_bp.route('/api', methods=['GET'])
@token_required
def get_ingrediente_materia_primas():
    relaciones = IngredienteMateriaPrima.query.all()
    return jsonify([{
        "id_ingrediente": r.id_ingrediente,
        "id_materia": r.id_materia,
        "cantidad_kg": float(r.cantidad_kg)
    } for r in relaciones])

@ingrediente_materia_prima_bp.route('/api/<int:id_ingrediente>/<int:id_materia>', methods=['GET'])
@token_required
def get_ingrediente_materia_prima(id_ingrediente, id_materia):
    relacion = IngredienteMateriaPrima.query.get_or_404((id_ingrediente, id_materia))
    return jsonify({
        "id_ingrediente": relacion.id_ingrediente,
        "id_materia": relacion.id_materia,
        "cantidad_kg": float(relacion.cantidad_kg)
    })

@ingrediente_materia_prima_bp.route('/api', methods=['POST'])
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

@ingrediente_materia_prima_bp.route('/api/<int:id_ingrediente>/<int:id_materia>', methods=['PUT'])
@token_required
def update_ingrediente_materia_prima(id_ingrediente, id_materia):
    relacion = IngredienteMateriaPrima.query.get_or_404((id_ingrediente, id_materia))
    data = request.get_json()
    relacion.cantidad_kg = data.get('cantidad_kg', relacion.cantidad_kg)
    db.session.commit()
    return jsonify({"message": "Ingrediente materia prima updated"})

@ingrediente_materia_prima_bp.route('/api/<int:id_ingrediente>/<int:id_materia>', methods=['DELETE'])
@token_required
def delete_ingrediente_materia_prima(id_ingrediente, id_materia):
    relacion = IngredienteMateriaPrima.query.get_or_404((id_ingrediente, id_materia))
    db.session.delete(relacion)
    db.session.commit()
    return jsonify({"message": "Ingrediente materia prima deleted"})

# --------------------------
# HTML CRUD ROUTES
# --------------------------
@ingrediente_materia_prima_bp.route('/', methods=['GET'])
@login_required
def index():
    relaciones = IngredienteMateriaPrima.query.all()
    return render_template('ingrediente_materia_prima/index.html', relaciones=relaciones)

@ingrediente_materia_prima_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        data = request.form
        nueva = IngredienteMateriaPrima(
            id_ingrediente=data.get('id_ingrediente'),
            id_materia=data.get('id_materia'),
            cantidad_kg=data.get('cantidad_kg')
        )
        db.session.add(nueva)
        db.session.commit()
        flash('Relación creada exitosamente.', 'success')
        return redirect(url_for('ingrediente_materia_prima.index'))
    return render_template('ingrediente_materia_prima/create.html')

@ingrediente_materia_prima_bp.route('/<int:id_ingrediente>/<int:id_materia>/update', methods=['GET', 'POST'])
@login_required
def update(id_ingrediente, id_materia):
    rel = IngredienteMateriaPrima.query.get_or_404((id_ingrediente, id_materia))
    if request.method == 'POST':
        data = request.form
        rel.cantidad_kg = data.get('cantidad_kg', rel.cantidad_kg)
        db.session.commit()
        flash('Relación actualizada exitosamente.', 'success')
        return redirect(url_for('ingrediente_materia_prima.index'))
    return render_template('ingrediente_materia_prima/update.html', r=rel)

@ingrediente_materia_prima_bp.route('/<int:id_ingrediente>/<int:id_materia>/delete', methods=['GET', 'POST'])
@login_required
def delete_html(id_ingrediente, id_materia):
    rel = IngredienteMateriaPrima.query.get_or_404((id_ingrediente, id_materia))
    if request.method == 'POST':
        db.session.delete(rel)
        db.session.commit()
        flash('Relación eliminada exitosamente.', 'success')
        return redirect(url_for('ingrediente_materia_prima.index'))
    return render_template('ingrediente_materia_prima/delete.html', r=rel)
