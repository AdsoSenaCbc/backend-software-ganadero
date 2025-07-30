from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.materia_prima import MateriaPrima
from app.utils.jwt_utils import token_required

materia_prima_bp = Blueprint('materia_prima', __name__)

@materia_prima_bp.route('/api', methods=['GET'])
@token_required
def get_materias_primas():
    materias = MateriaPrima.query.all()
    return jsonify([{
        "id_materia": m.id_materia,
        "nombre": m.nombre,
        "fuente": m.fuente,
        "descripcion": m.descripcion
    } for m in materias])

@materia_prima_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_materia_prima(id):
    materia = MateriaPrima.query.get_or_404(id)
    return jsonify({
        "id_materia": materia.id_materia,
        "nombre": materia.nombre,
        "fuente": materia.fuente,
        "descripcion": materia.descripcion
    })

@materia_prima_bp.route('/api', methods=['POST'])
@token_required
def create_materia_prima():
    data = request.get_json()
    new_materia = MateriaPrima(
        nombre=data.get('nombre'),
        fuente=data.get('fuente'),
        descripcion=data.get('descripcion')
    )
    db.session.add(new_materia)
    db.session.commit()
    return jsonify({"message": "Materia prima created", "id": new_materia.id_materia}), 201

@materia_prima_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_materia_prima(id):
    materia = MateriaPrima.query.get_or_404(id)
    data = request.get_json()
    materia.nombre = data.get('nombre', materia.nombre)
    materia.fuente = data.get('fuente', materia.fuente)
    materia.descripcion = data.get('descripcion', materia.descripcion)
    db.session.commit()
    return jsonify({"message": "Materia prima updated"})

@materia_prima_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_materia_prima(id):
    materia = MateriaPrima.query.get_or_404(id)
    db.session.delete(materia)
    db.session.commit()
    return jsonify({"message": "Materia prima deleted"})

# --------------------------
# HTML CRUD ROUTES
# --------------------------
@materia_prima_bp.route('/', methods=['GET'])
@login_required
def index():
    materias = MateriaPrima.query.all()
    return render_template('materia_prima/index.html', materias=materias)

@materia_prima_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        data = request.form
        nueva = MateriaPrima(nombre=data.get('nombre'), fuente=data.get('fuente'), descripcion=data.get('descripcion'))
        db.session.add(nueva)
        db.session.commit()
        flash('Materia prima creada exitosamente.', 'success')
        return redirect(url_for('materia_prima.index'))
    return render_template('materia_prima/create.html')

@materia_prima_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    materia = MateriaPrima.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        materia.nombre = data.get('nombre', materia.nombre)
        materia.fuente = data.get('fuente', materia.fuente)
        materia.descripcion = data.get('descripcion', materia.descripcion)
        db.session.commit()
        flash('Materia prima actualizada exitosamente.', 'success')
        return redirect(url_for('materia_prima.index'))
    return render_template('materia_prima/update.html', m=materia)

@materia_prima_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_html(id):
    materia = MateriaPrima.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(materia)
        db.session.commit()
        flash('Materia prima eliminada exitosamente.', 'success')
        return redirect(url_for('materia_prima.index'))
    return render_template('materia_prima/delete.html', m=materia)