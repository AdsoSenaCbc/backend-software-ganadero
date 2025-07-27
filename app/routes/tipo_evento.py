from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.tipo_evento import TipoEvento
from app.utils.jwt_utils import token_required

tipo_evento_bp = Blueprint('tipo_evento', __name__)

# --------------------------
# API JSON ENDPOINTS
# --------------------------
@tipo_evento_bp.route('/api', methods=['GET'])
@token_required
def get_tipos_evento_api():
    tipos = TipoEvento.query.all()
    return jsonify([{
        "id_tipo_evento": t.id_tipo_evento,
        "nombre_tipo": t.nombre_tipo
    } for t in tipos])

@tipo_evento_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_tipo_evento_api(id):
    t = TipoEvento.query.get_or_404(id)
    return jsonify({
        "id_tipo_evento": t.id_tipo_evento,
        "nombre_tipo": t.nombre_tipo
    })

@tipo_evento_bp.route('/api', methods=['POST'])
@token_required
def create_tipo_evento_api():
    data = request.get_json()
    new_tipo = TipoEvento(
        nombre_tipo=data.get('nombre_tipo')
    )
    db.session.add(new_tipo)
    db.session.commit()
    return jsonify({"message": "Tipo evento created", "id": new_tipo.id_tipo_evento}), 201

@tipo_evento_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_tipo_evento_api(id):
    tipo = TipoEvento.query.get_or_404(id)
    data = request.get_json()
    tipo.nombre_tipo = data.get('nombre_tipo', tipo.nombre_tipo)
    db.session.commit()
    return jsonify({"message": "Tipo evento updated"})

@tipo_evento_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_tipo_evento_api(id):
    tipo = TipoEvento.query.get_or_404(id)
    db.session.delete(tipo)
    db.session.commit()
    return jsonify({"message": "Tipo evento deleted"})

# --------------------------
# WEB ROUTES
# --------------------------
@tipo_evento_bp.route('/', methods=['GET'])
@login_required
def index():
    tipos = TipoEvento.query.all()
    return render_template('tipo_evento/index.html', tipos=tipos)

@tipo_evento_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        data = request.form
        new_tipo = TipoEvento(
            id_tipo_evento=data.get('id_tipo_evento'),
            nombre_tipo=data.get('nombre_tipo')
        )
        db.session.add(new_tipo)
        db.session.commit()
        flash('Tipo de evento creado exitosamente.', 'success')
        return redirect(url_for('tipo_evento.index'))
    return render_template('tipo_evento/create.html')

@tipo_evento_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    tipo = TipoEvento.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        tipo.id_tipo_evento = data.get('id_tipo_evento', tipo.id_tipo_evento)
        tipo.nombre_tipo = data.get('nombre_tipo', tipo.nombre_tipo)
        db.session.commit()
        flash('Tipo de evento actualizado exitosamente.', 'success')
        return redirect(url_for('tipo_evento.index'))
    return render_template('tipo_evento/update.html', tipo=tipo)

@tipo_evento_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    tipo = TipoEvento.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(tipo)
        db.session.commit()
        flash('Tipo de evento eliminado exitosamente.', 'success')
        return redirect(url_for('tipo_evento.index'))
    return render_template('tipo_evento/delete.html', tipo=tipo)