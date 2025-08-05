from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.detalle_racion_nutricional import DetalleRacionNutricional
from app.models.racion import Racion
from app.models.nutrientes import Nutrientes
from app.utils.jwt_utils import token_required

detalle_racion_nutricional_bp = Blueprint('detalle_racion_nutricional', __name__, url_prefix='/detalle-racion-nutricional')

# --------------------------
# API JSON ENDPOINTS
# --------------------------

@detalle_racion_nutricional_bp.route('/api', methods=['GET'])
@token_required
def get_detalles_api():
    detalles = DetalleRacionNutricional.query.all()
    return jsonify([{
        "id_detalle_nut": d.id_detalle_nut,
        "id_racion": d.id_racion,
        "id_nutriente": d.id_nutriente,
        "valor_aportado": float(d.valor_aportado)
    } for d in detalles])

@detalle_racion_nutricional_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_detalle_api(id):
    detalle = DetalleRacionNutricional.query.get_or_404(id)
    return jsonify({
        "id_detalle_nut": detalle.id_detalle_nut,
        "id_racion": detalle.id_racion,
        "id_nutriente": detalle.id_nutriente,
        "valor_aportado": float(detalle.valor_aportado)
    })

@detalle_racion_nutricional_bp.route('/api', methods=['POST'])
@token_required
def create_detalle_racion_nutricional():
    data = request.get_json()
    new_detalle = DetalleRacionNutricional(
        id_racion=data.get('id_racion'),
        id_nutriente=data.get('id_nutriente'),
        valor_aportado=data.get('valor_aportado')
    )
    db.session.add(new_detalle)
    db.session.commit()
    return jsonify({"message": "Detalle racion nutricional created", "id": new_detalle.id_detalle_nut}), 201

@detalle_racion_nutricional_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_detalle_racion_nutricional(id):
    detalle = DetalleRacionNutricional.query.get_or_404(id)
    data = request.get_json()
    detalle.id_racion = data.get('id_racion', detalle.id_racion)
    detalle.id_nutriente = data.get('id_nutriente', detalle.id_nutriente)
    detalle.valor_aportado = data.get('valor_aportado', detalle.valor_aportado)
    db.session.commit()
    return jsonify({"message": "Detalle racion nutricional updated"})

@detalle_racion_nutricional_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_detalle_racion_nutricional(id):
    detalle = DetalleRacionNutricional.query.get_or_404(id)
    db.session.delete(detalle)
    db.session.commit()
    return jsonify({"message": "Detalle racion nutricional deleted"})

# --------------------------
# HTML CRUD ROUTES
# --------------------------
from flask_login import login_required

@detalle_racion_nutricional_bp.route('/', methods=['GET'])
@login_required
def index_html():
    detalles = DetalleRacionNutricional.query.all()
    raciones_lookup = {r.id_racion: r for r in Racion.query.all()}
    nutrientes_lookup = {n.id_nutriente: n for n in Nutrientes.query.all()}
    return render_template('detalle_racion_nutricional/index.html', detalles=detalles, raciones_lookup=raciones_lookup, nutrientes_lookup=nutrientes_lookup)

@detalle_racion_nutricional_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_html():
    if request.method == 'POST':
        data = request.form
        nuevo = DetalleRacionNutricional(
            id_racion=data.get('id_racion'),
            id_nutriente=data.get('id_nutriente'),
            valor_aportado=data.get('valor_aportado')
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Detalle nutricional creado.', 'success')
        return redirect(url_for('detalle_racion_nutricional.index_html'))
    raciones = Racion.query.all()
    nutrientes = Nutrientes.query.all()
    return render_template('detalle_racion_nutricional/create.html', raciones=raciones, nutrientes=nutrientes)

@detalle_racion_nutricional_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_html(id):
    det = DetalleRacionNutricional.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        det.id_racion = data.get('id_racion', det.id_racion)
        det.id_nutriente = data.get('id_nutriente', det.id_nutriente)
        det.valor_aportado = data.get('valor_aportado', det.valor_aportado)
        db.session.commit()
        flash('Detalle nutricional actualizado.', 'success')
        return redirect(url_for('detalle_racion_nutricional.index_html'))
    raciones = Racion.query.all()
    nutrientes = Nutrientes.query.all()
    return render_template('detalle_racion_nutricional/update.html', det=det, raciones=raciones, nutrientes=nutrientes)

@detalle_racion_nutricional_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_html(id):
    det = DetalleRacionNutricional.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(det)
        db.session.commit()
        flash('Detalle nutricional eliminado.', 'success')
        return redirect(url_for('detalle_racion_nutricional.index_html'))
    return render_template('detalle_racion_nutricional/delete.html', det=det)
