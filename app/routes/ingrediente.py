from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.ingrediente import Ingrediente
from app.utils.jwt_utils import token_required

ingrediente_bp = Blueprint('ingrediente', __name__)

@ingrediente_bp.route('/api', methods=['GET'])
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

@ingrediente_bp.route('/api/<int:id>', methods=['GET'])
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

@ingrediente_bp.route('/api', methods=['POST'])
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

@ingrediente_bp.route('/api/<int:id>', methods=['PUT'])
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

@ingrediente_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_ingrediente(id):
    ingrediente = Ingrediente.query.get_or_404(id)
    db.session.delete(ingrediente)
    db.session.commit()
    return jsonify({"message": "Ingrediente deleted"})

# --------------------------
# HTML CRUD ROUTES
# --------------------------
@ingrediente_bp.route('/', methods=['GET'])
@login_required
def index():
    ingredientes = Ingrediente.query.all()
    return render_template('ingrediente/index.html', ingredientes=ingredientes)

@ingrediente_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        data = request.form
        nuevo = Ingrediente(
            nombre=data.get('nombre'),
            tipo=data.get('tipo'),
            descripcion=data.get('descripcion'),
            costo_kg=data.get('costo_kg')
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Ingrediente creado exitosamente.', 'success')
        return redirect(url_for('ingrediente.index'))
    return render_template('ingrediente/create.html')

@ingrediente_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    ing = Ingrediente.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        ing.nombre = data.get('nombre', ing.nombre)
        ing.tipo = data.get('tipo', ing.tipo)
        ing.descripcion = data.get('descripcion', ing.descripcion)
        ing.costo_kg = data.get('costo_kg', ing.costo_kg)
        db.session.commit()
        flash('Ingrediente actualizado exitosamente.', 'success')
        return redirect(url_for('ingrediente.index'))
    return render_template('ingrediente/update.html', i=ing)

@ingrediente_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_html(id):
    ing = Ingrediente.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(ing)
        db.session.commit()
        flash('Ingrediente eliminado exitosamente.', 'success')
        return redirect(url_for('ingrediente.index'))
    return render_template('ingrediente/delete.html', i=ing)