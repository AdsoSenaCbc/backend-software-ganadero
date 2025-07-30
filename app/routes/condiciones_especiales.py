from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.condiciones_especiales import CondicionesEspeciales
from app.utils.jwt_utils import token_required

condiciones_especiales_bp = Blueprint('condiciones_especiales', __name__)

# --------------------------
# API JSON ENDPOINTS
# --------------------------

@condiciones_especiales_bp.route('/api', methods=['GET'])
@token_required
def get_condiciones_api():
    condiciones = CondicionesEspeciales.query.all()
    return jsonify([{
        "id_condicion": c.id_condicion,
        "nombre": c.nombre,
        "descripcion": c.descripcion,
        "ajuste_nutriente": float(c.ajuste_nutriente)
    } for c in condiciones])

@condiciones_especiales_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_condicion_api(id):
    condicion = CondicionesEspeciales.query.get_or_404(id)
    return jsonify({
        "id_condicion": condicion.id_condicion,
        "nombre": condicion.nombre,
        "descripcion": condicion.descripcion,
        "ajuste_nutriente": float(condicion.ajuste_nutriente)
    })

@condiciones_especiales_bp.route('/api', methods=['POST'])
@token_required
def create_condicion_especial():
    data = request.get_json()
    new_condicion = CondicionesEspeciales(
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion'),
        ajuste_nutriente=data.get('ajuste_nutriente')
    )
    db.session.add(new_condicion)
    db.session.commit()
    return jsonify({"message": "Condicion especial created", "id": new_condicion.id_condicion}), 201

@condiciones_especiales_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_condicion_especial(id):
    condicion = CondicionesEspeciales.query.get_or_404(id)
    data = request.get_json()
    condicion.nombre = data.get('nombre', condicion.nombre)
    condicion.descripcion = data.get('descripcion', condicion.descripcion)
    condicion.ajuste_nutriente = data.get('ajuste_nutriente', condicion.ajuste_nutriente)
    db.session.commit()
    return jsonify({"message": "Condicion especial updated"})

@condiciones_especiales_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_condicion_especial(id):
    condicion = CondicionesEspeciales.query.get_or_404(id)
    db.session.delete(condicion)
    db.session.commit()
    return jsonify({"message": "Condicion especial deleted"})

# --------------------------
# HTML CRUD ROUTES
# --------------------------
from flask_login import login_required

@condiciones_especiales_bp.route('/', methods=['GET'])
@login_required
def index_html():
    condiciones = CondicionesEspeciales.query.all()
    return render_template('condiciones_especiales/index.html', condiciones=condiciones)

@condiciones_especiales_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_html():
    if request.method == 'POST':
        data = request.form
        nueva = CondicionesEspeciales(
            nombre=data.get('nombre'),
            descripcion=data.get('descripcion'),
            ajuste_nutriente=data.get('ajuste_nutriente')
        )
        db.session.add(nueva)
        db.session.commit()
        flash('Condición especial creada.', 'success')
        return redirect(url_for('condiciones_especiales.index_html'))
    return render_template('condiciones_especiales/create.html')

@condiciones_especiales_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_html(id):
    cond = CondicionesEspeciales.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        cond.nombre = data.get('nombre', cond.nombre)
        cond.descripcion = data.get('descripcion', cond.descripcion)
        cond.ajuste_nutriente = data.get('ajuste_nutriente', cond.ajuste_nutriente)
        db.session.commit()
        flash('Condición especial actualizada.', 'success')
        return redirect(url_for('condiciones_especiales.index_html'))
    return render_template('condiciones_especiales/update.html', cond=cond)

@condiciones_especiales_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_html(id):
    cond = CondicionesEspeciales.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(cond)
        db.session.commit()
        flash('Condición especial eliminada.', 'success')
        return redirect(url_for('condiciones_especiales.index_html'))
    return render_template('condiciones_especiales/delete.html', cond=cond)