from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_jwt_extended import jwt_required
from app.utils.jwt_utils import token_required
from flask_login import login_required
from app import db
from app.models.sales_minerales import SalesMinerales

sales_minerales_bp = Blueprint('sales_minerales', __name__)

# --------------------------
# API JSON ENDPOINTS
# --------------------------

@sales_minerales_bp.route('/api', methods=['GET'])
@token_required
def get_sales_api():
    sales = SalesMinerales.query.all()
    return jsonify([{ "id_sale_mineral": s.id_sale_mineral, "nombre": s.nombre, "composicion": s.composicion, "contenido_principal": float(s.contenido_principal) if s.contenido_principal else None, "uso_principal": s.uso_principal, "costo_kg": float(s.costo_kg) if s.costo_kg else None } for s in sales])

@sales_minerales_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_sale_api(id):
    s = SalesMinerales.query.get_or_404(id)
    return jsonify({ "id_sale_mineral": s.id_sale_mineral, "nombre": s.nombre, "composicion": s.composicion, "contenido_principal": float(s.contenido_principal) if s.contenido_principal else None, "uso_principal": s.uso_principal, "costo_kg": float(s.costo_kg) if s.costo_kg else None })

@sales_minerales_bp.route('/api', methods=['POST'])
@token_required
def create_sale_api():
    data = request.get_json()
    nuevo = SalesMinerales(nombre=data.get('nombre'), uso_principal=data.get('uso_principal'), costo_kg=data.get('costo_kg'))
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"message": "Sal mineral creada", "id": nuevo.id_sale_mineral}), 201

@sales_minerales_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_sale_api(id):
    s = SalesMinerales.query.get_or_404(id)
    data = request.get_json()
    s.nombre = data.get('nombre', s.nombre)
    s.uso_principal = data.get('uso_principal', s.uso_principal)
    s.costo_kg = data.get('costo_kg', s.costo_kg)
    db.session.commit()
    return jsonify({"message": "Sal mineral actualizada"})

@sales_minerales_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_sale_api(id):
    s = SalesMinerales.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    return jsonify({"message": "Sal mineral eliminada"})

# --------------------------
# HTML CRUD ROUTES
# --------------------------

@sales_minerales_bp.route('/', methods=['GET'])
@login_required
def index():
    sales = SalesMinerales.query.all()
    return render_template('sales_minerales/index.html', sales_minerales=sales)

@sales_minerales_bp.route('/index')
@jwt_required()
def index_jwt():
    sales = SalesMinerales.query.all()
    return render_template('sales_minerales/index.html', sales_minerales=sales)

# --------------------------
# HTML CREATE
# --------------------------
@sales_minerales_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_html():
    if request.method == 'POST':
        data = request.form
        nuevo = SalesMinerales(
            nombre=data.get('nombre'),
            uso_principal=data.get('uso_principal'),
            costo_kg=data.get('costo_kg')
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('Sal mineral creada.', 'success')
        return redirect(url_for('sales_minerales.index'))
    return render_template('sales_minerales/create.html')

# --------------------------
# HTML UPDATE
# --------------------------
@sales_minerales_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_html(id):
    sale = SalesMinerales.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        sale.nombre = data.get('nombre', sale.nombre)
        sale.uso_principal = data.get('uso_principal', sale.uso_principal)
        sale.costo_kg = data.get('costo_kg', sale.costo_kg)
        db.session.commit()
        flash('Sal mineral actualizada.', 'success')
        return redirect(url_for('sales_minerales.index'))
    return render_template('sales_minerales/update.html', sale=sale)

# --------------------------
# HTML DELETE
# --------------------------
@sales_minerales_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_html(id):
    sale = SalesMinerales.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(sale)
        db.session.commit()
        flash('Sal mineral eliminada.', 'success')
        return redirect(url_for('sales_minerales.index'))
    return render_template('sales_minerales/delete.html', sale=sale)