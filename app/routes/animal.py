from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.utils.jwt_utils import token_required
from app.models.animal import Animal
from app import db

animal_bp = Blueprint('animal', __name__)

# --------------------------
# API JSON ENDPOINTS
# --------------------------
@animal_bp.route('/api', methods=['GET'])
@token_required
def get_animals_api():
    animals = Animal.query.all()
    return jsonify([
        {
            "id": a.id_animal,
            "identificador_unico": a.identificador_unico,
            "nombre": a.nombre,
            "peso": float(a.peso) if a.peso else None,
        } for a in animals
    ])

@animal_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_animal_api(id):
    a = Animal.query.get_or_404(id)
    return jsonify({
        "id": a.id_animal,
        "identificador_unico": a.identificador_unico,
        "nombre": a.nombre,
        "peso": float(a.peso) if a.peso else None,
        "id_hacienda": a.id_hacienda,
        "id_raza": a.id_raza,
        "id_sexo": a.id_sexo,
        "id_especie": a.id_especie,
        "id_estado": a.id_estado,
        "id_etapa": a.id_etapa,
        "observaciones": a.observaciones,
    })

@animal_bp.route('/', methods=['GET'])
@login_required
def index():
    from app import db
    animals = Animal.query.all()
    return render_template('animals/index.html', animals=animals)

@animal_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    from app import db
    if request.method == 'POST':
        data = request.form
        new_animal = Animal(
            identificador_unico=data.get('identificador_unico'),
            nombre=data.get('nombre'),
            id_hacienda=data.get('id_hacienda'),
            id_raza=data.get('id_raza'),
            id_sexo=data.get('id_sexo'),
            id_especie=data.get('id_especie'),
            id_estado=data.get('id_estado'),
            id_etapa=data.get('id_etapa'),
            peso=data.get('peso'),
            observaciones=data.get('observaciones')
        )
        db.session.add(new_animal)
        db.session.commit()
        flash('Animal creado exitosamente.', 'success')
        return redirect(url_for('animal.index'))
    # GET: cargar listas para selects
    from app.models.hacienda import Hacienda
    from app.models.raza import Raza
    from app.models.sexo import Sexo
    from app.models.especie import Especie
    from app.models.estado_animal import EstadoAnimal
    from app.models.etapas_productivas import EtapasProductivas

    haciendas = Hacienda.query.all()
    razas = Raza.query.all()
    sexos = Sexo.query.all()
    especies = Especie.query.all()
    estados = EstadoAnimal.query.all()
    etapas = EtapasProductivas.query.all()
    return render_template('animals/create.html', haciendas=haciendas, razas=razas, sexos=sexos, especies=especies, estados=estados, etapas=etapas)

@animal_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    from app import db
    animal = Animal.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        animal.identificador_unico = data.get('identificador_unico', animal.identificador_unico)
        animal.nombre = data.get('nombre', animal.nombre)
        animal.id_hacienda = data.get('id_hacienda', animal.id_hacienda)
        animal.id_raza = data.get('id_raza', animal.id_raza)
        animal.id_sexo = data.get('id_sexo', animal.id_sexo)
        animal.id_especie = data.get('id_especie', animal.id_especie)
        animal.id_estado = data.get('id_estado', animal.id_estado)
        animal.id_etapa = data.get('id_etapa', animal.id_etapa)
        animal.peso = data.get('peso', animal.peso)
        animal.observaciones = data.get('observaciones', animal.observaciones)
        db.session.commit()
        flash('Animal actualizado exitosamente.', 'success')
        return redirect(url_for('animal.index'))
    # GET: cargar listas para selects
    from app.models.hacienda import Hacienda
    from app.models.raza import Raza
    from app.models.sexo import Sexo
    from app.models.especie import Especie
    from app.models.estado_animal import EstadoAnimal
    from app.models.etapas_productivas import EtapasProductivas

    haciendas = Hacienda.query.all()
    razas = Raza.query.all()
    sexos = Sexo.query.all()
    especies = Especie.query.all()
    estados = EstadoAnimal.query.all()
    etapas = EtapasProductivas.query.all()
    return render_template('animals/update.html', animal=animal, haciendas=haciendas, razas=razas, sexos=sexos, especies=especies, estados=estados, etapas=etapas)

@animal_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    from app import db
    animal = Animal.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(animal)
        db.session.commit()
        flash('Animal eliminado exitosamente.', 'success')
        return redirect(url_for('animal.index'))
    return render_template('animals/delete.html', animal=animal)