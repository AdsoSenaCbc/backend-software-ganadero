from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.caracteristicas_nutricionales import CaracteristicasNutricionales
from app.models.ingrediente import Ingrediente
from app.models.nutrientes import Nutrientes
from app.utils.jwt_utils import token_required

caracteristicas_nutricionales_bp = Blueprint('caracteristicas_nutricionales', __name__, url_prefix='/caracteristicas_nutricionales')

@caracteristicas_nutricionales_bp.route('/', methods=['GET'])
@token_required
def index():
    caracteristicas = CaracteristicasNutricionales.query.all()
    return jsonify([{
        "id_caracteristica": c.id_caracteristica,
        "id_ingrediente": c.id_ingrediente,
        "id_nutriente": c.id_nutriente,
        "valor": float(c.valor)
    } for c in caracteristicas])

@caracteristicas_nutricionales_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_caracteristica_nutricional(id):
    caracteristica = CaracteristicasNutricionales.query.get_or_404(id)
    return jsonify({
        "id_caracteristica": caracteristica.id_caracteristica,
        "id_ingrediente": caracteristica.id_ingrediente,
        "id_nutriente": caracteristica.id_nutriente,
        "valor": float(caracteristica.valor)
    })

@caracteristicas_nutricionales_bp.route('/', methods=['POST'])
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

@caracteristicas_nutricionales_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_caracteristica_nutricional(id):
    caracteristica = CaracteristicasNutricionales.query.get_or_404(id)
    data = request.get_json()
    caracteristica.id_ingrediente = data.get('id_ingrediente', caracteristica.id_ingrediente)
    caracteristica.id_nutriente = data.get('id_nutriente', caracteristica.id_nutriente)
    caracteristica.valor = data.get('valor', caracteristica.valor)
    db.session.commit()
    return jsonify({"message": "Caracteristica nutricional updated"})

@caracteristicas_nutricionales_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_caracteristica_nutricional(id):
    caracteristica = CaracteristicasNutricionales.query.get_or_404(id)
    db.session.delete(caracteristica)
    db.session.commit()
    return jsonify({"message": "Caracteristica nutricional deleted"})

# Web Routes
@caracteristicas_nutricionales_bp.route('/web', methods=['GET'])
@login_required
def index_web():
    # Obtener todas las características nutricionales con información de ingrediente y nutriente
    caracteristicas = db.session.query(
        CaracteristicasNutricionales,
        Ingrediente.nombre.label('nombre_ingrediente'),
        Nutrientes.nombre.label('nombre_nutriente'),
        Nutrientes.unidad
    ).join(
        Ingrediente, CaracteristicasNutricionales.id_ingrediente == Ingrediente.id_ingrediente
    ).join(
        Nutrientes, CaracteristicasNutricionales.id_nutriente == Nutrientes.id_nutriente
    ).all()
    
    return render_template('caracteristicas_nutricionales/index.html', 
                         caracteristicas=caracteristicas)

@caracteristicas_nutricionales_bp.route('/web/create', methods=['GET'])
@login_required
def create_web():
    # Obtener listas de ingredientes y nutrientes para los selects
    ingredientes = Ingrediente.query.order_by(Ingrediente.nombre).all()
    nutrientes = Nutrientes.query.order_by(Nutrientes.nombre).all()
    return render_template('caracteristicas_nutricionales/create.html',
                         ingredientes=ingredientes,
                         nutrientes=nutrientes)

@caracteristicas_nutricionales_bp.route('/web/create', methods=['POST'])
@login_required
def create_post_web():
    try:
        id_ingrediente = request.form.get('id_ingrediente')
        id_nutriente = request.form.get('id_nutriente')
        valor = request.form.get('valor')
        
        # Validaciones
        if not all([id_ingrediente, id_nutriente, valor]):
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('caracteristicas_nutricionales.create_web'))
            
        # Verificar si ya existe la relación
        if CaracteristicasNutricionales.query.filter_by(
            id_ingrediente=id_ingrediente, 
            id_nutriente=id_nutriente
        ).first():
            flash('Ya existe una característica nutricional para este ingrediente y nutriente', 'error')
            return redirect(url_for('caracteristicas_nutricionales.create_web'))
            
        # Crear nueva característica nutricional
        nueva_caracteristica = CaracteristicasNutricionales(
            id_ingrediente=id_ingrediente,
            id_nutriente=id_nutriente,
            valor=valor
        )
        
        db.session.add(nueva_caracteristica)
        db.session.commit()
        
        flash('Característica nutricional creada exitosamente', 'success')
        return redirect(url_for('caracteristicas_nutricionales.index_web'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear la característica nutricional: {str(e)}', 'error')
        return redirect(url_for('caracteristicas_nutricionales.create_web'))

@caracteristicas_nutricionales_bp.route('/web/<int:id>/edit', methods=['GET'])
@login_required
def edit_web(id):
    caracteristica = CaracteristicasNutricionales.query.get_or_404(id)
    ingredientes = Ingrediente.query.order_by(Ingrediente.nombre).all()
    nutrientes = Nutrientes.query.order_by(Nutrientes.nombre).all()
    
    return render_template('caracteristicas_nutricionales/update.html',
                         caracteristica=caracteristica,
                         ingredientes=ingredientes,
                         nutrientes=nutrientes)

@caracteristicas_nutricionales_bp.route('/web/<int:id>/edit', methods=['POST'])
@login_required
def update_web(id):
    try:
        caracteristica = CaracteristicasNutricionales.query.get_or_404(id)
        id_ingrediente = request.form.get('id_ingrediente')
        id_nutriente = request.form.get('id_nutriente')
        valor = request.form.get('valor')
        
        # Validaciones
        if not all([id_ingrediente, id_nutriente, valor]):
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('caracteristicas_nutricionales.edit_web', id=id))
            
        # Verificar si ya existe otra característica con el mismo par ingrediente-nutriente
        existing = CaracteristicasNutricionales.query.filter(
            CaracteristicasNutricionales.id_ingrediente == id_ingrediente,
            CaracteristicasNutricionales.id_nutriente == id_nutriente,
            CaracteristicasNutricionales.id_caracteristica != id
        ).first()
        
        if existing:
            flash('Ya existe una característica nutricional para este ingrediente y nutriente', 'error')
            return redirect(url_for('caracteristicas_nutricionales.edit_web', id=id))
            
        # Actualizar la característica
        caracteristica.id_ingrediente = id_ingrediente
        caracteristica.id_nutriente = id_nutriente
        caracteristica.valor = valor
        
        db.session.commit()
        
        flash('Característica nutricional actualizada exitosamente', 'success')
        return redirect(url_for('caracteristicas_nutricionales.index_web'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al actualizar la característica nutricional: {str(e)}', 'error')
        return redirect(url_for('caracteristicas_nutricionales.edit_web', id=id))

@caracteristicas_nutricionales_bp.route('/web/<int:id>/delete', methods=['GET'])
@login_required
def delete_web(id):
    try:
        caracteristica = CaracteristicasNutricionales.query.get_or_404(id)
        db.session.delete(caracteristica)
        db.session.commit()
        flash('Característica nutricional eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la característica nutricional: {str(e)}', 'error')
    return redirect(url_for('caracteristicas_nutricionales.index_web'))