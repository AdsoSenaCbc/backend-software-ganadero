from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.requerimientos_nutricionales import RequerimientosNutricionales
from app.models.etapas_productivas import EtapasProductivas
from app.models.nutrientes import Nutrientes
from app.utils.jwt_utils import token_required

requerimientos_nutricionales_bp = Blueprint('requerimientos_nutricionales', __name__, url_prefix='/requerimientos-nutricionales')

# --------------------------
# API JSON ENDPOINTS
# --------------------------

@requerimientos_nutricionales_bp.route('/api', methods=['GET'])
@token_required
def get_requerimientos_api():
    requerimientos = RequerimientosNutricionales.query.all()
    return jsonify([{
        "id_requerimiento": r.id_requerimiento,
        "id_etapa": r.id_etapa,
        "peso_min": float(r.peso_min),
        "peso_max": float(r.peso_max),
        "id_nutriente": r.id_nutriente,
        "valor_min": float(r.valor_min),
        "valor_max": float(r.valor_max),
        "condicion": r.condicion
    } for r in requerimientos])

@requerimientos_nutricionales_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_requerimiento_api(id):
    requerimiento = RequerimientosNutricionales.query.get_or_404(id)
    return jsonify({
        "id_requerimiento": requerimiento.id_requerimiento,
        "id_etapa": requerimiento.id_etapa,
        "peso_min": float(requerimiento.peso_min),
        "peso_max": float(requerimiento.peso_max),
        "id_nutriente": requerimiento.id_nutriente,
        "valor_min": float(requerimiento.valor_min),
        "valor_max": float(requerimiento.valor_max),
        "condicion": requerimiento.condicion
    })

@requerimientos_nutricionales_bp.route('/api', methods=['POST'])
@token_required
def create_requerimiento_nutricional():
    data = request.get_json()
    new_requerimiento = RequerimientosNutricionales(
        id_etapa=data.get('id_etapa'),
        peso_min=data.get('peso_min'),
        peso_max=data.get('peso_max'),
        id_nutriente=data.get('id_nutriente'),
        valor_min=data.get('valor_min'),
        valor_max=data.get('valor_max'),
        condicion=data.get('condicion')
    )
    db.session.add(new_requerimiento)
    db.session.commit()
    return jsonify({"message": "Requerimiento nutricional created", "id": new_requerimiento.id_requerimiento}), 201

@requerimientos_nutricionales_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_requerimiento_nutricional(id):
    requerimiento = RequerimientosNutricionales.query.get_or_404(id)
    data = request.get_json()
    requerimiento.id_etapa = data.get('id_etapa', requerimiento.id_etapa)
    requerimiento.peso_min = data.get('peso_min', requerimiento.peso_min)
    requerimiento.peso_max = data.get('peso_max', requerimiento.peso_max)
    requerimiento.id_nutriente = data.get('id_nutriente', requerimiento.id_nutriente)
    requerimiento.valor_min = data.get('valor_min', requerimiento.valor_min)
    requerimiento.valor_max = data.get('valor_max', requerimiento.valor_max)
    requerimiento.condicion = data.get('condicion', requerimiento.condicion)
    db.session.commit()
    return jsonify({"message": "Requerimiento nutricional updated"})

@requerimientos_nutricionales_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_requerimiento_nutricional(id):
    requerimiento = RequerimientosNutricionales.query.get_or_404(id)
    db.session.delete(requerimiento)
    db.session.commit()
    return jsonify({"message": "Requerimiento nutricional deleted"})

# --------------------------
# HTML CRUD ROUTES
# --------------------------
from flask_login import login_required

@requerimientos_nutricionales_bp.route('/', methods=['GET'])
@login_required
def index_html():
    requerimientos = RequerimientosNutricionales.query.all()
    return render_template('requerimientos_nutricionales/index.html', requerimientos=requerimientos)

@requerimientos_nutricionales_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_html():
    if request.method == 'POST':
        data = request.form
        nuevo = RequerimientosNutricionales(
            id_etapa=data.get('id_etapa'),
            peso_min=data.get('peso_min'),
            peso_max=data.get('peso_max'),
            id_nutriente=data.get('id_nutriente'),
            valor_min=data.get('valor_min'),
            valor_max=data.get('valor_max'),
            condicion=data.get('condicion')
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Requerimiento nutricional creado.', 'success')
        return redirect(url_for('requerimientos_nutricionales.index_html'))
    return render_template('requerimientos_nutricionales/create.html')

@requerimientos_nutricionales_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_html(id):
    req = RequerimientosNutricionales.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        req.id_etapa = data.get('id_etapa', req.id_etapa)
        req.peso_min = data.get('peso_min', req.peso_min)
        req.peso_max = data.get('peso_max', req.peso_max)
        req.id_nutriente = data.get('id_nutriente', req.id_nutriente)
        req.valor_min = data.get('valor_min', req.valor_min)
        req.valor_max = data.get('valor_max', req.valor_max)
        req.condicion = data.get('condicion', req.condicion)
        db.session.commit()
        flash('Requerimiento nutricional actualizado.', 'success')
        return redirect(url_for('requerimientos_nutricionales.index_html'))
    return render_template('requerimientos_nutricionales/update.html', req=req)

@requerimientos_nutricionales_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_html(id):
    req = RequerimientosNutricionales.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(req)
        db.session.commit()
        flash('Requerimiento nutricional eliminado.', 'success')
        return redirect(url_for('requerimientos_nutricionales.index_html'))
    return render_template('requerimientos_nutricionales/delete.html', req=req)
