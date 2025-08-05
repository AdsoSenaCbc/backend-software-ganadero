from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.consulta_bromatologica import ConsultaBromatologica
from app.models.usuario import Usuario
from app.utils.jwt_utils import token_required

consulta_bromatologica_bp = Blueprint('consulta_bromatologica', __name__)

# --------------------------
# API JSON ENDPOINTS
# --------------------------

@consulta_bromatologica_bp.route('/api', methods=['GET'])
@token_required
def get_consultas_api():
    consultas = ConsultaBromatologica.query.all()
    return jsonify([{
        "id_consulta": c.id_consulta,
        "fecha_consulta": c.fecha_consulta.isoformat(),
        "id_usuario": c.id_usuario
    } for c in consultas])

@consulta_bromatologica_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_consulta_api(id):
    consulta = ConsultaBromatologica.query.get_or_404(id)
    return jsonify({
        "id_consulta": consulta.id_consulta,
        "fecha_consulta": consulta.fecha_consulta.isoformat(),
        "id_usuario": consulta.id_usuario
    })

@consulta_bromatologica_bp.route('/api', methods=['POST'])
@token_required
def create_consulta_bromatologica():
    data = request.get_json()
    new_consulta = ConsultaBromatologica(
        id_usuario=data.get('id_usuario')
    )
    db.session.add(new_consulta)
    db.session.commit()
    return jsonify({"message": "Consulta bromatologica created", "id": new_consulta.id_consulta}), 201

@consulta_bromatologica_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_consulta_bromatologica(id):
    consulta = ConsultaBromatologica.query.get_or_404(id)
    data = request.get_json()
    consulta.id_usuario = data.get('id_usuario', consulta.id_usuario)
    db.session.commit()
    return jsonify({"message": "Consulta bromatologica updated"})

@consulta_bromatologica_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_consulta_bromatologica(id):
    consulta = ConsultaBromatologica.query.get_or_404(id)
    db.session.delete(consulta)
    db.session.commit()
    return jsonify({"message": "Consulta bromatologica deleted"})

# --------------------------
# HTML CRUD ROUTES
# --------------------------
from flask_login import login_required

@consulta_bromatologica_bp.route('/', methods=['GET'])
@login_required
def index_html():
    consultas = ConsultaBromatologica.query.all()
    usuarios_lookup = {u.id_usuario: u for u in Usuario.query.all()}
    return render_template('consulta_bromatologica/index.html', consultas=consultas, usuarios_lookup=usuarios_lookup)

@consulta_bromatologica_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_html():
    if request.method == 'POST':
        data = request.form
        from datetime import datetime
        fecha_str = data.get('fecha_consulta')
        fecha = datetime.fromisoformat(fecha_str) if fecha_str else None
        nueva = ConsultaBromatologica(id_usuario=data.get('id_usuario'), fecha_consulta=fecha)
        db.session.add(nueva)
        db.session.commit()
        flash('Consulta creada.', 'success')
        return redirect(url_for('consulta_bromatologica.index_html'))
    usuarios = Usuario.query.all()
    return render_template('consulta_bromatologica/create.html', usuarios=usuarios)

@consulta_bromatologica_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_html(id):
    cons = ConsultaBromatologica.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        from datetime import datetime
        cons.id_usuario = data.get('id_usuario', cons.id_usuario)
        fecha_str = data.get('fecha_consulta')
        if fecha_str:
            cons.fecha_consulta = datetime.fromisoformat(fecha_str)
        db.session.commit()
        flash('Consulta actualizada.', 'success')
        return redirect(url_for('consulta_bromatologica.index_html'))
    usuarios = Usuario.query.all()
    return render_template('consulta_bromatologica/update.html', cons=cons, usuarios=usuarios)

@consulta_bromatologica_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_html(id):
    cons = ConsultaBromatologica.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(cons)
        db.session.commit()
        flash('Consulta eliminada.', 'success')
        return redirect(url_for('consulta_bromatologica.index_html'))
    return render_template('consulta_bromatologica/delete.html', cons=cons)