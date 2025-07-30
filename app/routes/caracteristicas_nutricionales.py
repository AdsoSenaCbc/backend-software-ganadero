from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.caracteristicas_nutricionales import CaracteristicasNutricionales
from app.utils.jwt_utils import token_required

caracteristicas_nutricionales_bp = Blueprint('caracteristicas_nutricionales', __name__)

@caracteristicas_nutricionales_bp.route('/api', methods=['GET'])
@token_required
def api_index():
    caracteristicas = CaracteristicasNutricionales.query.all()
    return jsonify([{
        "id_caracteristica": c.id_caracteristica,
        "id_ingrediente": c.id_ingrediente,
        "id_nutriente": c.id_nutriente,
        "valor": float(c.valor)
    } for c in caracteristicas])

@caracteristicas_nutricionales_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_caracteristica_nutricional(id):
    caracteristica = CaracteristicasNutricionales.query.get_or_404(id)
    return jsonify({
        "id_caracteristica": caracteristica.id_caracteristica,
        "id_ingrediente": caracteristica.id_ingrediente,
        "id_nutriente": caracteristica.id_nutriente,
        "valor": float(caracteristica.valor)
    })

@caracteristicas_nutricionales_bp.route('/api', methods=['POST'])
@token_required
def create_caracteristica_nutricional():
    data = request.get_json()
    new_caracteristica = CaracteristicasNutricionales(
        id_ingrediente=data.get('id_ingrediente'),
        id_nutriente=data.get('id_nutriente'),
        valor=data.get('valor')
    )
    db.session.add(new_caracteristica)
    db.session.commit()
    return jsonify({"message": "Caracteristica nutricional created", "id": new_caracteristica.id_caracteristica}), 201

@caracteristicas_nutricionales_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_caracteristica_nutricional(id):
    caracteristica = CaracteristicasNutricionales.query.get_or_404(id)
    data = request.get_json()
    caracteristica.id_ingrediente = data.get('id_ingrediente', caracteristica.id_ingrediente)
    caracteristica.id_nutriente = data.get('id_nutriente', caracteristica.id_nutriente)
    caracteristica.valor = data.get('valor', caracteristica.valor)
    db.session.commit()
    return jsonify({"message": "Caracteristica nutricional updated"})

@caracteristicas_nutricionales_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_caracteristica_nutricional(id):
    caracteristica = CaracteristicasNutricionales.query.get_or_404(id)
    db.session.delete(caracteristica)
    db.session.commit()
    return jsonify({"message": "Caracteristica nutricional deleted"})

# --------------------------
# HTML CRUD ROUTES
# --------------------------
@caracteristicas_nutricionales_bp.route('/', methods=['GET'])
@login_required
def index_html():
    caracteristicas = CaracteristicasNutricionales.query.all()
    return render_template('caracteristicas_nutricionales/index.html', caracteristicas=caracteristicas)

@caracteristicas_nutricionales_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_html():
    if request.method == 'POST':
        data = request.form
        nueva = CaracteristicasNutricionales(
            id_ingrediente=data.get('id_ingrediente'),
            id_nutriente=data.get('id_nutriente'),
            valor=data.get('valor')
        )
        db.session.add(nueva)
        db.session.commit()
        flash('Característica nutricional creada.', 'success')
        return redirect(url_for('caracteristicas_nutricionales.index_html'))
    return render_template('caracteristicas_nutricionales/create.html')

@caracteristicas_nutricionales_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_html(id):
    c = CaracteristicasNutricionales.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        c.id_ingrediente = data.get('id_ingrediente', c.id_ingrediente)
        c.id_nutriente = data.get('id_nutriente', c.id_nutriente)
        c.valor = data.get('valor', c.valor)
        db.session.commit()
        flash('Característica nutricional actualizada.', 'success')
        return redirect(url_for('caracteristicas_nutricionales.index_html'))
    return render_template('caracteristicas_nutricionales/update.html', c=c)

@caracteristicas_nutricionales_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_html(id):
    c = CaracteristicasNutricionales.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(c)
        db.session.commit()
        flash('Característica nutricional eliminada.', 'success')
        return redirect(url_for('caracteristicas_nutricionales.index_html'))
    return render_template('caracteristicas_nutricionales/delete.html', c=c)