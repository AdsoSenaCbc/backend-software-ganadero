from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.utils.jwt_utils import token_required
from app.models.sexo import Sexo
from app import db

sexo_bp = Blueprint('sexo', __name__)

# --------------------------
# API JSON ENDPOINTS
# --------------------------
@sexo_bp.route('/api', methods=['GET'])
@token_required
def get_sexos_api():
    sexos = Sexo.query.all()
    return jsonify([
        {
            "id_sexo": s.id_sexo,
            "nombre": s.nombre,
        } for s in sexos
    ])

@sexo_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_sexo_api(id):
    s = Sexo.query.get_or_404(id)
    return jsonify({
        "id_sexo": s.id_sexo,
        "nombre": s.nombre,
    })

# --------------------------
# WEB ROUTES
# --------------------------
@sexo_bp.route('/', methods=['GET'])
@login_required
def index():
    sexos = Sexo.query.all()
    return render_template('sexo/index.html', sexos=sexos)

@sexo_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        data = request.form
        new_sexo = Sexo(
            id_sexo=data.get('id_sexo'),
            nombre=data.get('nombre')
        )
        db.session.add(new_sexo)
        db.session.commit()
        flash('Sexo creado exitosamente.', 'success')
        return redirect(url_for('sexo.index'))
    return render_template('sexo/create.html')

@sexo_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    sexo = Sexo.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        sexo.id_sexo = data.get('id_sexo', sexo.id_sexo)
        sexo.nombre = data.get('nombre', sexo.nombre)
        db.session.commit()
        flash('Sexo actualizado exitosamente.', 'success')
        return redirect(url_for('sexo.index'))
    return render_template('sexo/update.html', sexo=sexo)

@sexo_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    sexo = Sexo.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(sexo)
        db.session.commit()
        flash('Sexo eliminado exitosamente.', 'success')
        return redirect(url_for('sexo.index'))
    return render_template('sexo/delete.html', sexo=sexo)