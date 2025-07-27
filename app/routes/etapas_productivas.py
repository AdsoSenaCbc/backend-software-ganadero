from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.etapas_productivas import EtapasProductivas
from app.utils.jwt_utils import token_required

etapas_productivas_bp = Blueprint('etapas_productivas', __name__, url_prefix='/api/etapas-productivas')

@etapas_productivas_bp.route('/', methods=['GET'])
@token_required
def get_etapas_productivas():
    etapas = EtapasProductivas.query.all()
    return jsonify([{
        "id_etapa": e.id_etapa,
        "nombre": e.nombre,
        "descripcion": e.descripcion
    } for e in etapas])

@etapas_productivas_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_etapa_productiva(id):
    etapa = EtapasProductivas.query.get_or_404(id)
    return jsonify({
        "id_etapa": etapa.id_etapa,
        "nombre": etapa.nombre,
        "descripcion": etapa.descripcion
    })

@etapas_productivas_bp.route('/', methods=['POST'])
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

@etapas_productivas_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_etapa_productiva(id):
    etapa = EtapasProductivas.query.get_or_404(id)
    data = request.get_json()
    etapa.nombre = data.get('nombre', etapa.nombre)
    etapa.descripcion = data.get('descripcion', etapa.descripcion)
    db.session.commit()
    return jsonify({"message": "Etapa productiva updated"})

@etapas_productivas_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_etapa_productiva(id):
    etapa = EtapasProductivas.query.get_or_404(id)
    db.session.delete(etapa)
    db.session.commit()
    return jsonify({"message": "Etapa productiva deleted"})

# ==============================================
# RUTAS WEB
# ==============================================

@etapas_productivas_bp.route('/web', methods=['GET'])
@etapas_productivas_bp.route('/', methods=['GET'])
@login_required
def index():
    etapas = EtapasProductivas.query.all()
    return render_template('etapas_productivas/index.html', etapas=etapas)

@etapas_productivas_bp.route('/web/create', methods=['GET'])
@login_required
def create_web():
    return render_template('etapas_productivas/create.html')

@etapas_productivas_bp.route('/web/create', methods=['POST'])
@login_required
def create_post_web():
    try:
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion', '')
        
        if not nombre:
            flash('El nombre es obligatorio', 'error')
            return redirect(url_for('etapas_productivas.create_web'))
            
        # Verificar si ya existe una etapa con el mismo nombre
        if EtapasProductivas.query.filter_by(nombre=nombre).first():
            flash('Ya existe una etapa con este nombre', 'error')
            return redirect(url_for('etapas_productivas.create_web'))
            
        nueva_etapa = EtapasProductivas(
            nombre=nombre,
            descripcion=descripcion
        )
        
        db.session.add(nueva_etapa)
        db.session.commit()
        
        flash('Etapa productiva creada exitosamente', 'success')
        return redirect(url_for('etapas_productivas.index_web'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear la etapa productiva: {str(e)}', 'error')
        return redirect(url_for('etapas_productivas.create_web'))

@etapas_productivas_bp.route('/web/<int:id>/edit', methods=['GET'])
@login_required
def edit_web(id):
    etapa = EtapasProductivas.query.get_or_404(id)
    return render_template('etapas_productivas/update.html', etapa=etapa)

@etapas_productivas_bp.route('/web/<int:id>/update', methods=['POST'])
@login_required
def update_web(id):
    try:
        etapa = EtapasProductivas.query.get_or_404(id)
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion', '')
        
        if not nombre:
            flash('El nombre es obligatorio', 'error')
            return redirect(url_for('etapas_productivas.edit_web', id=id))
            
        # Verificar si ya existe otra etapa con el mismo nombre
        if EtapasProductivas.query.filter(EtapasProductivas.nombre == nombre, EtapasProductivas.id_etapa != id).first():
            flash('Ya existe otra etapa con este nombre', 'error')
            return redirect(url_for('etapas_productivas.edit_web', id=id))
            
        etapa.nombre = nombre
        etapa.descripcion = descripcion
        
        db.session.commit()
        
        flash('Etapa productiva actualizada exitosamente', 'success')
        return redirect(url_for('etapas_productivas.index_web'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar la etapa productiva: {str(e)}', 'error')
        return redirect(url_for('etapas_productivas.edit_web', id=id))

@etapas_productivas_bp.route('/web/<int:id>/delete', methods=['GET'])
@login_required
def delete_web(id):
    try:
        etapa = EtapasProductivas.query.get_or_404(id)
        
        # Verificar si hay animales asociados a esta etapa
        if etapa.animals:
            flash('No se puede eliminar esta etapa porque tiene animales asociados', 'error')
            return redirect(url_for('etapas_productivas.index_web'))
            
        # Verificar si hay requerimientos nutricionales asociados
        if etapa.requerimientos:
            flash('No se puede eliminar esta etapa porque tiene requerimientos nutricionales asociados', 'error')
            return redirect(url_for('etapas_productivas.index_web'))
        
        db.session.delete(etapa)
        db.session.commit()
        
        flash('Etapa productiva eliminada exitosamente', 'success')
        return redirect(url_for('etapas_productivas.index_web'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la etapa productiva: {str(e)}', 'error')
        return redirect(url_for('etapas_productivas.index_web'))