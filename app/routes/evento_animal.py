from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.evento_animal import EventoAnimal
from app.utils.jwt_utils import token_required
from flask_login import login_required

evento_animal_bp = Blueprint('evento_animal', __name__)

# --------------------------
# HTML FORM ROUTES
# --------------------------
@evento_animal_bp.route('/', methods=['GET'])
@login_required
def index():
    eventos = EventoAnimal.query.all()
    return render_template('evento_animal/index.html', eventos=eventos)

@evento_animal_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_evento():
    if request.method == 'POST':
        id_animal = request.form.get('id_animal')
        id_evento = request.form.get('id_evento')
        id_tipo_evento = request.form.get('id_tipo_evento')
        fecha_evento = request.form.get('fecha_evento')
        valor = request.form.get('valor')
        observaciones = request.form.get('observaciones')
        if not (id_animal and id_evento and id_tipo_evento):
            flash('Campos obligatorios faltantes', 'danger')
            return redirect(url_for('evento_animal.create_evento'))
        nuevo = EventoAnimal(id_animal=id_animal, id_evento=id_evento, id_tipo_evento=id_tipo_evento, fecha_evento=fecha_evento, valor=valor, observaciones=observaciones)
        db.session.add(nuevo)
        db.session.commit()
        flash('Evento creado correctamente.', 'success')
        return redirect(url_for('evento_animal.index'))
    return render_template('evento_animal/create.html')

@evento_animal_bp.route('/<int:id_animal>/<int:id_evento>/update', methods=['GET', 'POST'])
@login_required
def update_evento(id_animal, id_evento):
    evento = EventoAnimal.query.get_or_404((id_animal, id_evento))
    if request.method == 'POST':
        evento.id_tipo_evento = request.form.get('id_tipo_evento', evento.id_tipo_evento)
        evento.fecha_evento = request.form.get('fecha_evento', evento.fecha_evento)
        evento.valor = request.form.get('valor', evento.valor)
        evento.observaciones = request.form.get('observaciones', evento.observaciones)
        db.session.commit()
        flash('Evento actualizado correctamente.', 'success')
        return redirect(url_for('evento_animal.index'))
    return render_template('evento_animal/update.html', evento=evento)

@evento_animal_bp.route('/<int:id_animal>/<int:id_evento>/delete', methods=['GET', 'POST'])
@login_required
def delete_evento(id_animal, id_evento):
    evento = EventoAnimal.query.get_or_404((id_animal, id_evento))
    if request.method == 'POST':
        db.session.delete(evento)
        db.session.commit()
        flash('Evento eliminado correctamente.', 'success')
        return redirect(url_for('evento_animal.index'))
    return render_template('evento_animal/delete.html', evento=evento)

# --------------------------
# API JSON ENDPOINTS
# --------------------------
@evento_animal_bp.route('/api', methods=['GET'])
@token_required
def get_eventos_api():
    eventos = EventoAnimal.query.all()
    return jsonify([{
        "id_animal": e.id_animal,
        "id_evento": e.id_evento,
        "id_tipo_evento": e.id_tipo_evento,
        "fecha_evento": e.fecha_evento.isoformat(),
        "valor": float(e.valor),
        "observaciones": e.observaciones
    } for e in eventos])

@evento_animal_bp.route('/api/<int:id_animal>/<int:id_evento>', methods=['GET'])
@token_required
def get_evento_api(id_animal, id_evento):
    evento = EventoAnimal.query.get_or_404((id_animal, id_evento))
    return jsonify({
        "id_animal": evento.id_animal,
        "id_evento": evento.id_evento,
        "id_tipo_evento": evento.id_tipo_evento,
        "fecha_evento": evento.fecha_evento.isoformat(),
        "valor": float(evento.valor),
        "observaciones": evento.observaciones
    })

@evento_animal_bp.route('/api', methods=['POST'])
@token_required
def create_evento_api():
    data = request.get_json()
    new_evento = EventoAnimal(
        id_animal=data.get('id_animal'),
        id_evento=data.get('id_evento'),
        id_tipo_evento=data.get('id_tipo_evento'),
        valor=data.get('valor'),
        observaciones=data.get('observaciones')
    )
    db.session.add(new_evento)
    db.session.commit()
    return jsonify({"message": "Evento animal created", "id_animal": new_evento.id_animal, "id_evento": new_evento.id_evento}), 201

@evento_animal_bp.route('/api/<int:id_animal>/<int:id_evento>', methods=['PUT'])
@token_required
def update_evento_api(id_animal, id_evento):
    evento = EventoAnimal.query.get_or_404((id_animal, id_evento))
    data = request.get_json()
    evento.id_tipo_evento = data.get('id_tipo_evento', evento.id_tipo_evento)
    evento.valor = data.get('valor', evento.valor)
    evento.observaciones = data.get('observaciones', evento.observaciones)
    db.session.commit()
    return jsonify({"message": "Evento animal updated"})

@evento_animal_bp.route('/api/<int:id_animal>/<int:id_evento>', methods=['DELETE'])
@token_required
def delete_evento_api(id_animal, id_evento):
    evento = EventoAnimal.query.get_or_404((id_animal, id_evento))
    db.session.delete(evento)
    db.session.commit()
    return jsonify({"message": "Evento animal deleted"})