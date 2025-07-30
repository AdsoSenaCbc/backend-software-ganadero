from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.sexo import Sexo
from app.utils.jwt_utils import token_required
from flask_login import login_required

sexo_bp = Blueprint('sexo', __name__)

# --------------------------
# HTML FORM ROUTES
# --------------------------
@sexo_bp.route('/', methods=['GET'])
@login_required
def index():
    sexos = Sexo.query.all()
    return render_template('sexo/index.html', sexos=sexos)

@sexo_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_sexo_form():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if not nombre:
            flash('El nombre es obligatorio', 'danger')
            return redirect(url_for('sexo.create_sexo_form'))
        nuevo = Sexo(nombre=nombre)
        db.session.add(nuevo)
        db.session.commit()
        flash('Sexo creado correctamente.', 'success')
        return redirect(url_for('sexo.index'))
    return render_template('sexo/create.html')

@sexo_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_sexo_form(id):
    sexo = Sexo.query.get_or_404(id)
    if request.method == 'POST':
        sexo.nombre = request.form.get('nombre', sexo.nombre)
        db.session.commit()
        flash('Sexo actualizado correctamente.', 'success')
        return redirect(url_for('sexo.index'))
    return render_template('sexo/update.html', sexo=sexo)

@sexo_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_sexo_form(id):
    sexo = Sexo.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(sexo)
        db.session.commit()
        flash('Sexo eliminado correctamente.', 'success')
        return redirect(url_for('sexo.index'))
    return render_template('sexo/delete.html', sexo=sexo)

# --------------------------
# API JSON ENDPOINTS
# --------------------------
@sexo_bp.route('/api/sexos', methods=['GET'])
@token_required
def get_sexos_api():
    sexos = Sexo.query.all()
    return jsonify([{
        "id_sexo": s.id_sexo,
        "nombre": s.nombre
    } for s in sexos])

@sexo_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_sexo_api(id):
    sexo = Sexo.query.get_or_404(id)
    return jsonify({
        "id_sexo": sexo.id_sexo,
        "nombre": sexo.nombre
    })

@sexo_bp.route('/api', methods=['POST'])
@token_required
def create_sexo_api():
    data = request.get_json()
    new_sexo = Sexo(
        nombre=data.get('nombre')
    )
    db.session.add(new_sexo)
    db.session.commit()
    return jsonify({"message": "Sexo created", "id": new_sexo.id_sexo}), 201

@sexo_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_sexo_api(id):
    sexo = Sexo.query.get_or_404(id)
    data = request.get_json()
    sexo.nombre = data.get('nombre', sexo.nombre)
    db.session.commit()
    return jsonify({"message": "Sexo updated"})

@sexo_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_sexo_api(id):
    sexo = Sexo.query.get_or_404(id)
    db.session.delete(sexo)
    db.session.commit()
    return jsonify({"message": "Sexo deleted"})