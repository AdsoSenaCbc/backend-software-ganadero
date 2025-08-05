from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.historial_animal import HistorialAnimal
from app.models.animal import Animal
from app.models.hacienda import Hacienda
from app.utils.jwt_utils import token_required
from flask_login import login_required

historial_animal_bp = Blueprint('historial_animal', __name__)

@historial_animal_bp.route('/api', methods=['GET'])
@token_required
def get_historiales_api():
    historiales = HistorialAnimal.query.all()
    return jsonify([{
        "id_historial": h.id_historial,
        "id_animal": h.id_animal,
        "id_hacienda": h.id_hacienda,
        "fecha_ingreso": h.fecha_ingreso.isoformat(),
        "fecha_salida": h.fecha_salida.isoformat() if h.fecha_salida else None,
        "observaciones": h.observaciones
    } for h in historiales])

@historial_animal_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_historial_api(id):
    historial = HistorialAnimal.query.get_or_404(id)
    return jsonify({
        "id_historial": historial.id_historial,
        "id_animal": historial.id_animal,
        "id_hacienda": historial.id_hacienda,
        "fecha_ingreso": historial.fecha_ingreso.isoformat(),
        "fecha_salida": historial.fecha_salida.isoformat() if historial.fecha_salida else None,
        "observaciones": historial.observaciones
    })

@historial_animal_bp.route('/api', methods=['POST'])
@token_required
def create_historial_animal():
    data = request.get_json()
    new_historial = HistorialAnimal(
        id_animal=data.get('id_animal'),
        id_hacienda=data.get('id_hacienda'),
        fecha_salida=data.get('fecha_salida'),
        observaciones=data.get('observaciones')
    )
    db.session.add(new_historial)
    db.session.commit()
    return jsonify({"message": "Historial animal created", "id": new_historial.id_historial}), 201

@historial_animal_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_historial_animal(id):
    historial = HistorialAnimal.query.get_or_404(id)
    data = request.get_json()
    historial.id_animal = data.get('id_animal', historial.id_animal)
    historial.id_hacienda = data.get('id_hacienda', historial.id_hacienda)
    historial.fecha_salida = data.get('fecha_salida', historial.fecha_salida)
    historial.observaciones = data.get('observaciones', historial.observaciones)
    db.session.commit()
    return jsonify({"message": "Historial animal updated"})

@historial_animal_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_historial_animal(id):
    historial = HistorialAnimal.query.get_or_404(id)
    db.session.delete(historial)
    db.session.commit()
    return jsonify({"message": "Historial animal deleted"})

# --------------------------
# HTML CRUD ROUTES
# --------------------------
@historial_animal_bp.route('/', methods=['GET'])
@login_required
def index_html():
    historiales = HistorialAnimal.query.all()
    animals_lookup = {a.id_animal: a for a in Animal.query.all()}
    haciendas_lookup = {h.id_hacienda: h for h in Hacienda.query.all()}
    return render_template('historial_animal/index.html', historiales=historiales, animals_lookup=animals_lookup, haciendas_lookup=haciendas_lookup)

@historial_animal_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_html():
    if request.method == 'POST':
        data = request.form
        nuevo = HistorialAnimal(
            id_animal=data.get('id_animal'),
            id_hacienda=data.get('id_hacienda'),
            fecha_ingreso=data.get('fecha_ingreso'),
            fecha_salida=data.get('fecha_salida') or None,
            observaciones=data.get('observaciones')
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Historial creado.', 'success')
        return redirect(url_for('historial_animal.index_html'))
    animals = Animal.query.all()
    haciendas = Hacienda.query.all()
    return render_template('historial_animal/create.html', animals=animals, haciendas=haciendas)

@historial_animal_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_html(id):
    hist = HistorialAnimal.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        hist.id_animal = data.get('id_animal', hist.id_animal)
        hist.id_hacienda = data.get('id_hacienda', hist.id_hacienda)
        hist.fecha_ingreso = data.get('fecha_ingreso', hist.fecha_ingreso)
        hist.fecha_salida = data.get('fecha_salida', hist.fecha_salida)
        hist.observaciones = data.get('observaciones', hist.observaciones)
        db.session.commit()
        flash('Historial actualizado.', 'success')
        return redirect(url_for('historial_animal.index_html'))
    animals = Animal.query.all()
    haciendas = Hacienda.query.all()
    return render_template('historial_animal/update.html', hist=hist, animals=animals, haciendas=haciendas)

@historial_animal_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_html(id):
    hist = HistorialAnimal.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(hist)
        db.session.commit()
        flash('Historial eliminado.', 'success')
        return redirect(url_for('historial_animal.index_html'))
    return render_template('historial_animal/delete.html', hist=hist)