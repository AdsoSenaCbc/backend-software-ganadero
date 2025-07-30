from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.consulta_ingredientes import ConsultaIngredientes
from app.utils.jwt_utils import token_required

consulta_ingredientes_bp = Blueprint('consulta_ingredientes', __name__)

# --------------------------
# API JSON ENDPOINTS
# --------------------------

@consulta_ingredientes_bp.route('/api', methods=['GET'])
@token_required
def get_consultas_api():
    consultas = ConsultaIngredientes.query.all()
    return jsonify([{
        "id_consulta": c.id_consulta,
        "id_ingrediente": c.id_ingrediente,
        "resultado": c.resultado
    } for c in consultas])

@consulta_ingredientes_bp.route('/api/<int:id_consulta>/<int:id_ingrediente>', methods=['GET'])
@token_required
def get_consulta_api(id_consulta, id_ingrediente):
    consulta = ConsultaIngredientes.query.get_or_404((id_consulta, id_ingrediente))
    return jsonify({
        "id_consulta": consulta.id_consulta,
        "id_ingrediente": consulta.id_ingrediente,
        "resultado": consulta.resultado
    })

@consulta_ingredientes_bp.route('/api', methods=['POST'])
@token_required
def create_consulta_ingrediente():
    data = request.get_json()
    new_consulta = ConsultaIngredientes(
        id_consulta=data.get('id_consulta'),
        id_ingrediente=data.get('id_ingrediente'),
        resultado=data.get('resultado')
    )
    db.session.add(new_consulta)
    db.session.commit()
    return jsonify({"message": "Consulta ingrediente created", "id_consulta": new_consulta.id_consulta, "id_ingrediente": new_consulta.id_ingrediente}), 201

@consulta_ingredientes_bp.route('/api/<int:id_consulta>/<int:id_ingrediente>', methods=['PUT'])
@token_required
def update_consulta_ingrediente(id_consulta, id_ingrediente):
    consulta = ConsultaIngredientes.query.get_or_404((id_consulta, id_ingrediente))
    data = request.get_json()
    consulta.resultado = data.get('resultado', consulta.resultado)
    db.session.commit()
    return jsonify({"message": "Consulta ingrediente updated"})

@consulta_ingredientes_bp.route('/api/<int:id_consulta>/<int:id_ingrediente>', methods=['DELETE'])
@token_required
def delete_consulta_ingrediente(id_consulta, id_ingrediente):
    consulta = ConsultaIngredientes.query.get_or_404((id_consulta, id_ingrediente))
    db.session.delete(consulta)
    db.session.commit()
    return jsonify({"message": "Consulta ingrediente deleted"})

# --------------------------
# HTML CRUD ROUTES
# --------------------------
from flask_login import login_required

@consulta_ingredientes_bp.route('/', methods=['GET'])
@login_required
def index_html():
    consultas = ConsultaIngredientes.query.all()
    return render_template('consulta_ingredientes/index.html', consultas=consultas)

@consulta_ingredientes_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_html():
    if request.method == 'POST':
        data = request.form
        nueva = ConsultaIngredientes(
            id_consulta=data.get('id_consulta'),
            id_ingrediente=data.get('id_ingrediente'),
            resultado=data.get('resultado')
        )
        db.session.add(nueva)
        db.session.commit()
        flash('Consulta ingrediente creada.', 'success')
        return redirect(url_for('consulta_ingredientes.index_html'))
    return render_template('consulta_ingredientes/create.html')

@consulta_ingredientes_bp.route('/<int:id_consulta>/<int:id_ingrediente>/update', methods=['GET', 'POST'])
@login_required
def update_html(id_consulta, id_ingrediente):
    cons = ConsultaIngredientes.query.get_or_404((id_consulta, id_ingrediente))
    if request.method == 'POST':
        data = request.form
        cons.resultado = data.get('resultado', cons.resultado)
        db.session.commit()
        flash('Consulta ingrediente actualizada.', 'success')
        return redirect(url_for('consulta_ingredientes.index_html'))
    return render_template('consulta_ingredientes/update.html', cons=cons)

@consulta_ingredientes_bp.route('/<int:id_consulta>/<int:id_ingrediente>/delete', methods=['GET', 'POST'])
@login_required
def delete_html(id_consulta, id_ingrediente):
    cons = ConsultaIngredientes.query.get_or_404((id_consulta, id_ingrediente))
    if request.method == 'POST':
        db.session.delete(cons)
        db.session.commit()
        flash('Consulta ingrediente eliminada.', 'success')
        return redirect(url_for('consulta_ingredientes.index_html'))
    return render_template('consulta_ingredientes/delete.html', cons=cons)