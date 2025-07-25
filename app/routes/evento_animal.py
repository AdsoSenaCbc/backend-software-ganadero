from flask import Blueprint, request, jsonify
from app import db
from app.models.evento_animal import EventoAnimal
from app.utils.jwt_utils import token_required

evento_animal_bp = Blueprint('evento_animal', __name__)

@evento_animal_bp.route('/', methods=['GET'])
@token_required
def get_eventos_animal():
    eventos = EventoAnimal.query.all()
    return jsonify([{
        "id_animal": e.id_animal,
        "id_evento": e.id_evento,
        "id_tipo_evento": e.id_tipo_evento,
        "fecha_evento": e.fecha_evento.isoformat(),
        "valor": float(e.valor),
        "observaciones": e.observaciones
    } for e in eventos])

@evento_animal_bp.route('/<int:id_animal>/<int:id_evento>', methods=['GET'])
@token_required
def get_evento_animal(id_animal, id_evento):
    evento = EventoAnimal.query.get_or_404((id_animal, id_evento))
    return jsonify({
        "id_animal": evento.id_animal,
        "id_evento": evento.id_evento,
        "id_tipo_evento": evento.id_tipo_evento,
        "fecha_evento": evento.fecha_evento.isoformat(),
        "valor": float(evento.valor),
        "observaciones": evento.observaciones
    })

@evento_animal_bp.route('/', methods=['POST'])
@token_required
def create_evento_animal():
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

@evento_animal_bp.route('/<int:id_animal>/<int:id_evento>', methods=['PUT'])
@token_required
def update_evento_animal(id_animal, id_evento):
    evento = EventoAnimal.query.get_or_404((id_animal, id_evento))
    data = request.get_json()
    evento.id_tipo_evento = data.get('id_tipo_evento', evento.id_tipo_evento)
    evento.valor = data.get('valor', evento.valor)
    evento.observaciones = data.get('observaciones', evento.observaciones)
    db.session.commit()
    return jsonify({"message": "Evento animal updated"})

@evento_animal_bp.route('/<int:id_animal>/<int:id_evento>', methods=['DELETE'])
@token_required
def delete_evento_animal(id_animal, id_evento):
    evento = EventoAnimal.query.get_or_404((id_animal, id_evento))
    db.session.delete(evento)
    db.session.commit()
    return jsonify({"message": "Evento animal deleted"})