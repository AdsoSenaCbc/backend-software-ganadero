from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.requerimientos_nrc import RequerimientosNrc
from app.utils.jwt_utils import token_required

requerimientos_nrc_bp = Blueprint('requerimientos_nrc', __name__)

# --------------------------
# API JSON ENDPOINTS
# --------------------------
@requerimientos_nrc_bp.route('/api', methods=['GET'])
@token_required
def get_requerimientos_nrc():
    requerimientos = RequerimientosNrc.query.all()
    return jsonify([{
        "id": r.id,
        "etapa": r.etapa,
        "peso": float(r.peso),
        "produccion_leche": float(r.produccion_leche),
        "grasa_leche": float(r.grasa_leche),
        "em": float(r.em),
        "pc": float(r.pc),
        "ms": float(r.ms),
        "observaciones": r.observaciones
    } for r in requerimientos])

@requerimientos_nrc_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_requerimiento_nrc(id):
    requerimiento = RequerimientosNrc.query.get_or_404(id)
    return jsonify({
        "id": requerimiento.id,
        "etapa": requerimiento.etapa,
        "peso": float(requerimiento.peso),
        "produccion_leche": float(requerimiento.produccion_leche),
        "grasa_leche": float(requerimiento.grasa_leche),
        "em": float(requerimiento.em),
        "pc": float(requerimiento.pc),
        "ms": float(requerimiento.ms),
        "observaciones": requerimiento.observaciones
    })

@requerimientos_nrc_bp.route('/api', methods=['POST'])
@token_required
def create_requerimiento_nrc():
    data = request.get_json()
    new_requerimiento = RequerimientosNrc(
        etapa=data.get('etapa'),
        peso=data.get('peso'),
        produccion_leche=data.get('produccion_leche'),
        grasa_leche=data.get('grasa_leche'),
        em=data.get('em'),
        pc=data.get('pc'),
        ms=data.get('ms'),
        observaciones=data.get('observaciones')
    )
    db.session.add(new_requerimiento)
    db.session.commit()
    return jsonify({"message": "Requerimiento NRC created", "id": new_requerimiento.id}), 201

@requerimientos_nrc_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_requerimiento_nrc(id):
    requerimiento = RequerimientosNrc.query.get_or_404(id)
    data = request.get_json()
    requerimiento.etapa = data.get('etapa', requerimiento.etapa)
    requerimiento.peso = data.get('peso', requerimiento.peso)
    requerimiento.produccion_leche = data.get('produccion_leche', requerimiento.produccion_leche)
    requerimiento.grasa_leche = data.get('grasa_leche', requerimiento.grasa_leche)
    requerimiento.em = data.get('em', requerimiento.em)
    requerimiento.pc = data.get('pc', requerimiento.pc)
    requerimiento.ms = data.get('ms', requerimiento.ms)
    requerimiento.observaciones = data.get('observaciones', requerimiento.observaciones)
    db.session.commit()
    return jsonify({"message": "Requerimiento NRC updated"})

@requerimientos_nrc_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_requerimiento_nrc(id):
    requerimiento = RequerimientosNrc.query.get_or_404(id)
    db.session.delete(requerimiento)
    db.session.commit()
    return jsonify({"message": "Requerimiento NRC deleted"})

# --------------------------
# HTML CRUD ROUTES
# --------------------------
@requerimientos_nrc_bp.route('/', methods=['GET'])
@login_required
def index_html():
    from app.models.etapas_productivas import EtapasProductivas
    requerimientos = RequerimientosNrc.query.all()
    etapas = EtapasProductivas.query.all()
    etapas_lookup = {str(e.id_etapa): e.nombre for e in etapas}
    return render_template('requerimientos_nrc/index.html', requerimientos=requerimientos, etapas_lookup=etapas_lookup)

@requerimientos_nrc_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_html():
    from app.models.etapas_productivas import EtapasProductivas
    if request.method == 'POST':
        data = request.form
        nuevo = RequerimientosNrc(
            etapa=data.get('etapa'),
            peso=data.get('peso'),
            produccion_leche=data.get('produccion_leche'),
            grasa_leche=data.get('grasa_leche'),
            em=data.get('em'),
            pc=data.get('pc'),
            ms=data.get('ms'),
            observaciones=data.get('observaciones')
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Requerimiento NRC creado exitosamente.', 'success')
        return redirect(url_for('requerimientos_nrc.index_html'))
        from app.models.etapas_productivas import EtapasProductivas
    etapas = EtapasProductivas.query.all()
    return render_template('requerimientos_nrc/create.html', etapas=etapas)

@requerimientos_nrc_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_html(id):
    from app.models.etapas_productivas import EtapasProductivas
    req = RequerimientosNrc.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        req.etapa = data.get('etapa', req.etapa)
        req.peso = data.get('peso', req.peso)
        req.produccion_leche = data.get('produccion_leche', req.produccion_leche)
        req.grasa_leche = data.get('grasa_leche', req.grasa_leche)
        req.em = data.get('em', req.em)
        req.pc = data.get('pc', req.pc)
        req.ms = data.get('ms', req.ms)
        req.observaciones = data.get('observaciones', req.observaciones)
        db.session.commit()
        flash('Requerimiento NRC actualizado exitosamente.', 'success')
        return redirect(url_for('requerimientos_nrc.index_html'))
        from app.models.etapas_productivas import EtapasProductivas
    etapas = EtapasProductivas.query.all()
    return render_template('requerimientos_nrc/update.html', req=req, etapas=etapas)

@requerimientos_nrc_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_html(id):
    req = RequerimientosNrc.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(req)
        db.session.commit()
        flash('Requerimiento NRC eliminado exitosamente.', 'success')
        return redirect(url_for('requerimientos_nrc.index_html'))
    return render_template('requerimientos_nrc/delete.html', req=req)