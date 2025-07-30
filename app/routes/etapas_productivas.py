from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.etapas_productivas import EtapasProductivas
from app.utils.jwt_utils import token_required

etapas_productivas_bp = Blueprint('etapas_productivas', __name__)

# --------------------------
# API JSON ENDPOINTS
# --------------------------

@etapas_productivas_bp.route('/api', methods=['GET'])
@token_required
def get_etapas_api():
    etapas = EtapasProductivas.query.all()
    return jsonify([{
        "id_etapa": e.id_etapa,
        "nombre": e.nombre,
        "descripcion": e.descripcion
    } for e in etapas])

@etapas_productivas_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_etapa_api(id):
    etapa = EtapasProductivas.query.get_or_404(id)
    return jsonify({
        "id_etapa": etapa.id_etapa,
        "nombre": etapa.nombre,
        "descripcion": etapa.descripcion
    })

@etapas_productivas_bp.route('/api', methods=['POST'])
@token_required
def create_etapa_productiva():
    data = request.get_json()
    new_etapa = EtapasProductivas(
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion')
    )
    db.session.add(new_etapa)
    db.session.commit()
    return jsonify({"message": "Etapa productiva created", "id": new_etapa.id_etapa}), 201

@etapas_productivas_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_etapa_productiva(id):
    etapa = EtapasProductivas.query.get_or_404(id)
    data = request.get_json()
    etapa.nombre = data.get('nombre', etapa.nombre)
    etapa.descripcion = data.get('descripcion', etapa.descripcion)
    db.session.commit()
    return jsonify({"message": "Etapa productiva updated"})

@etapas_productivas_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_etapa_productiva(id):
    etapa = EtapasProductivas.query.get_or_404(id)
    db.session.delete(etapa)
    db.session.commit()
    return jsonify({"message": "Etapa productiva deleted"})

# --------------------------
# HTML CRUD ROUTES
# --------------------------
from flask_login import login_required

@etapas_productivas_bp.route('/', methods=['GET'])
@login_required
def index_html():
    etapas = EtapasProductivas.query.all()
    return render_template('etapas_productivas/index.html', etapas=etapas)

@etapas_productivas_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_html():
    if request.method == 'POST':
        data = request.form
        new_etapa = EtapasProductivas(
            nombre=data.get('nombre'),
            descripcion=data.get('descripcion')
        )
        db.session.add(new_etapa)
        db.session.commit()
        flash('Etapa productiva creada.', 'success')
        return redirect(url_for('etapas_productivas.index_html'))
    return render_template('etapas_productivas/create.html')

@etapas_productivas_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_html(id):
    etapa = EtapasProductivas.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        etapa.nombre = data.get('nombre', etapa.nombre)
        etapa.descripcion = data.get('descripcion', etapa.descripcion)
        db.session.commit()
        flash('Etapa productiva actualizada.', 'success')
        return redirect(url_for('etapas_productivas.index_html'))
    return render_template('etapas_productivas/update.html', etapa=etapa)

@etapas_productivas_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_html(id):
    etapa = EtapasProductivas.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(etapa)
        db.session.commit()
        flash('Etapa productiva eliminada.', 'success')
        return redirect(url_for('etapas_productivas.index_html'))
    return render_template('etapas_productivas/delete.html', etapa=etapa)