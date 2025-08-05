from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app.utils.jwt_utils import token_required
from flask_login import login_required
from app import db
from app.models.concentrados import Concentrados

concentrados_bp = Blueprint('concentrados', __name__)

# --------------------------
# API JSON ENDPOINTS
# --------------------------

@concentrados_bp.route('/api', methods=['GET'])
@token_required
def get_concentrados_api():
    concs = Concentrados.query.all()
    return jsonify([{ "id_concentrado": c.id_concentrado, "nombre": c.nombre, "tipo": c.tipo, "descripcion": c.descripcion, "costo_kg": float(c.costo_kg) if c.costo_kg is not None else None } for c in concs])

@concentrados_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_concentrado_api(id):
    c = Concentrados.query.get_or_404(id)
    return jsonify({ "id_concentrado": c.id_concentrado, "nombre": c.nombre, "tipo": c.tipo, "descripcion": c.descripcion, "costo_kg": float(c.costo_kg) if c.costo_kg is not None else None })

@concentrados_bp.route('/api', methods=['POST'])
@token_required
def create_concentrado_api():
    data = request.get_json()
    nuevo = Concentrados(nombre=data.get('nombre'), tipo=data.get('tipo'), descripcion=data.get('descripcion'), costo_kg=data.get('costo_kg'))
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"message": "Concentrado creado", "id": nuevo.id_concentrado}), 201

@concentrados_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_concentrado_api(id):
    c = Concentrados.query.get_or_404(id)
    data = request.get_json()
    c.nombre = data.get('nombre', c.nombre)
    c.tipo = data.get('tipo', c.tipo)
    c.descripcion = data.get('descripcion', c.descripcion)
    c.costo_kg = data.get('costo_kg', c.costo_kg)
    db.session.commit()
    return jsonify({"message": "Concentrado actualizado"})

@concentrados_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_concentrado_api(id):
    c = Concentrados.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    return jsonify({"message": "Concentrado eliminado"})

# --------------------------
# HTML CRUD ROUTES
# --------------------------

@concentrados_bp.route('/', methods=['GET'])
@login_required
def index():
    concentrados = Concentrados.query.all()
    return render_template('concentrados/index.html', concentrados=concentrados)

@concentrados_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_html():
    if request.method == 'POST':
        data = request.form
        nuevo = Concentrados(nombre=data.get('nombre'), tipo=data.get('tipo'), descripcion=data.get('descripcion'), costo_kg=data.get('costo_kg'))
        db.session.add(nuevo)
        db.session.commit()
        flash('Concentrado creado.', 'success')
        return redirect(url_for('concentrados.index'))
    return render_template('concentrados/create.html')

@concentrados_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_html(id):
    c = Concentrados.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        c.nombre = data.get('nombre', c.nombre)
        c.tipo = data.get('tipo', c.tipo)
        c.descripcion = data.get('descripcion', c.descripcion)
        c.costo_kg = data.get('costo_kg', c.costo_kg)
        db.session.commit()
        flash('Concentrado actualizado.', 'success')
        return redirect(url_for('concentrados.index'))
    return render_template('concentrados/update.html', conc=c)

@concentrados_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_html(id):
    c = Concentrados.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(c)
        db.session.commit()
        flash('Concentrado eliminado.', 'success')
        return redirect(url_for('concentrados.index'))
    return render_template('concentrados/delete.html', conc=c)

@concentrados_bp.route('/index_token')
@token_required
def index_token():
    concentrados = Concentrados.query.all()
    return render_template('concentrados/index.html', concentrados=concentrados)