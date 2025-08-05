from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.vacunacion_animal import VacunacionAnimal
from app.utils.jwt_utils import token_required
from flask_login import login_required
from datetime import datetime

vacunacion_animal_bp = Blueprint('vacunacion_animal', __name__)

# ------------------------- HTML ROUTES -------------------------
@vacunacion_animal_bp.route('/', methods=['GET'])
@login_required
def index():
    vacunaciones = VacunacionAnimal.query.all()
    return render_template('vacunacion_animal/index.html', vacunaciones=vacunaciones)

@vacunacion_animal_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_form():
    if request.method == 'POST':
        id_animal = request.form.get('id_animal')
        id_vacuna = request.form.get('id_vacuna')
        fecha = request.form.get('fecha_aplicacion')
        id_lote = request.form.get('id_lote')
        observaciones = request.form.get('observaciones')
        if not (id_animal and id_vacuna and fecha):
            flash('Campos obligatorios faltantes', 'danger')
            return redirect(url_for('vacunacion_animal.create_form'))
        nueva = VacunacionAnimal(id_animal=id_animal, id_vacuna=id_vacuna, fecha_aplicacion=fecha, id_lote=id_lote, observaciones=observaciones)
        db.session.add(nueva)
        db.session.commit()
        flash('Vacunación registrada', 'success')
        return redirect(url_for('vacunacion_animal.index'))
    # GET: cargar listas
    from app.models.animal import Animal
    from app.models.vacuna import Vacuna
    from app.models.lote_vacuna import LoteVacuna
    animals = Animal.query.all()
    vacunas = Vacuna.query.all()
    lotes = LoteVacuna.query.all()
    return render_template('vacunacion_animal/create.html', animals=animals, vacunas=vacunas, lotes=lotes)

@vacunacion_animal_bp.route('/<int:id_animal>/<int:id_vacuna>/<string:fecha>/update', methods=['GET', 'POST'])
@login_required
def update_form(id_animal, id_vacuna, fecha):
    fecha_dt = datetime.fromisoformat(fecha)
    vacunacion = VacunacionAnimal.query.get_or_404((id_animal, id_vacuna, fecha_dt))
    if request.method == 'POST':
        vacunacion.fecha_aplicacion = request.form.get('fecha_aplicacion', vacunacion.fecha_aplicacion)
        vacunacion.id_lote = request.form.get('id_lote', vacunacion.id_lote)
        vacunacion.observaciones = request.form.get('observaciones', vacunacion.observaciones)
        db.session.commit()
        flash('Vacunación actualizada', 'success')
        return redirect(url_for('vacunacion_animal.index'))
    from app.models.lote_vacuna import LoteVacuna
    lotes = LoteVacuna.query.all()
    return render_template('vacunacion_animal/update.html', v=vacunacion, lotes=lotes)

@vacunacion_animal_bp.route('/<int:id_animal>/<int:id_vacuna>/<string:fecha>/delete', methods=['GET', 'POST'])
@login_required
def delete_form(id_animal, id_vacuna, fecha):
    fecha_dt = datetime.fromisoformat(fecha)
    vacunacion = VacunacionAnimal.query.get_or_404((id_animal, id_vacuna, fecha_dt))
    if request.method == 'POST':
        db.session.delete(vacunacion)
        db.session.commit()
        flash('Vacunación eliminada', 'success')
        return redirect(url_for('vacunacion_animal.index'))
    return render_template('vacunacion_animal/delete.html', v=vacunacion)

# ------------------------- API ROUTES -------------------------

@vacunacion_animal_bp.route('/api/vacunaciones_animal', methods=['GET'])
@token_required
def get_vacunaciones_animal_api():
    vacunaciones = VacunacionAnimal.query.all()
    return jsonify([{
        "id_animal": v.id_animal,
        "id_vacuna": v.id_vacuna,
        "id_lote": v.id_lote,
        "fecha_aplicacion": v.fecha_aplicacion.isoformat(),
        "observaciones": v.observaciones
    } for v in vacunaciones])

@vacunacion_animal_bp.route('/api/<int:id_animal>/<int:id_vacuna>/<string:fecha>', methods=['GET'])
@token_required
def get_vacunacion_animal_api(id_animal, id_vacuna, fecha):
    vacunacion = VacunacionAnimal.query.get_or_404((id_animal, id_vacuna, datetime.fromisoformat(fecha)))
    return jsonify({
        "id_vacunacion": vacunacion.id_vacunacion,
        "id_animal": vacunacion.id_animal,
        "id_vacuna": vacunacion.id_vacuna,
        "id_lote": vacunacion.id_lote,
        "fecha_aplicacion": vacunacion.fecha_aplicacion.isoformat(),
        "observaciones": vacunacion.observaciones
    })

@vacunacion_animal_bp.route('/api/vacunaciones_animal', methods=['POST'])
@token_required
def create_vacunacion_animal_api():
    data = request.get_json()
    new_vacunacion = VacunacionAnimal(
        id_animal=data.get('id_animal'),
        id_vacuna=data.get('id_vacuna'),
        id_lote=data.get('id_lote'),
        observaciones=data.get('observaciones')
    )
    db.session.add(new_vacunacion)
    db.session.commit()
    return jsonify({"message": "Vacunacion animal created", "id": new_vacunacion.id_vacunacion}), 201

@vacunacion_animal_bp.route('/api/<int:id_animal>/<int:id_vacuna>/<string:fecha>', methods=['PUT'])
@token_required
def update_vacunacion_animal_api(id_animal, id_vacuna, fecha):
    vacunacion = VacunacionAnimal.query.get_or_404((id_animal, id_vacuna, datetime.fromisoformat(fecha)))
    data = request.get_json()
    vacunacion.id_animal = data.get('id_animal', vacunacion.id_animal)
    vacunacion.id_vacuna = data.get('id_vacuna', vacunacion.id_vacuna)
    vacunacion.id_lote = data.get('id_lote', vacunacion.id_lote)
    vacunacion.observaciones = data.get('observaciones', vacunacion.observaciones)
    db.session.commit()
    return jsonify({"message": "Vacunacion animal updated"})

@vacunacion_animal_bp.route('/api/<int:id_animal>/<int:id_vacuna>/<string:fecha>', methods=['DELETE'])
@token_required
def delete_vacunacion_animal_api(id_animal, id_vacuna, fecha):
    vacunacion = VacunacionAnimal.query.get_or_404((id_animal, id_vacuna, datetime.fromisoformat(fecha)))
    db.session.delete(vacunacion)
    db.session.commit()
    return jsonify({"message": "Vacunacion animal deleted"})