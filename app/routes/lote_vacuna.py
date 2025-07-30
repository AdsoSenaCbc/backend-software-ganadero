from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.lote_vacuna import LoteVacuna
from app.utils.jwt_utils import token_required
from flask_login import login_required

lote_vacuna_bp = Blueprint('lote_vacuna', __name__, url_prefix='/lote-vacuna')

# ------------------- HTML ROUTES -------------------
@lote_vacuna_bp.route('/', methods=['GET'])
@login_required
def index():
    lotes = LoteVacuna.query.all()
    return render_template('lote_vacuna/index.html', lotes=lotes)

@lote_vacuna_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_lote_form():
    if request.method == 'POST':
        codigo = request.form.get('codigo_lote')
        fecha = request.form.get('fecha_vencimiento')
        fabricante = request.form.get('fabricante')
        if not codigo:
            flash('El código de lote es obligatorio', 'danger')
            return redirect(url_for('lote_vacuna.create_lote_form'))
        nuevo = LoteVacuna(codigo_lote=codigo, fecha_vencimiento=fecha, fabricante=fabricante)
        db.session.add(nuevo)
        db.session.commit()
        flash('Lote de vacuna creado correctamente', 'success')
        return redirect(url_for('lote_vacuna.index'))
    return render_template('lote_vacuna/create.html')

@lote_vacuna_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_lote_form(id):
    lote = LoteVacuna.query.get_or_404(id)
    if request.method == 'POST':
        lote.codigo_lote = request.form.get('codigo_lote', lote.codigo_lote)
        lote.fecha_vencimiento = request.form.get('fecha_vencimiento', lote.fecha_vencimiento)
        lote.fabricante = request.form.get('fabricante', lote.fabricante)
        db.session.commit()
        flash('Lote de vacuna actualizado', 'success')
        return redirect(url_for('lote_vacuna.index'))
    return render_template('lote_vacuna/update.html', lote=lote)

@lote_vacuna_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_lote_form(id):
    lote = LoteVacuna.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(lote)
        db.session.commit()
        flash('Lote de vacuna eliminado', 'success')
        return redirect(url_for('lote_vacuna.index'))
    return render_template('lote_vacuna/delete.html', lote=lote)

# ------------------- API ROUTES -------------------

@lote_vacuna_bp.route('/api/lotes_vacuna', methods=['GET'])
@token_required
def get_lotes_vacuna_api():
    lotes = LoteVacuna.query.all()
    return jsonify([{
        "id_lote": l.id_lote,
        "codigo_lote": l.codigo_lote,
        "fecha_vencimiento": l.fecha_vencimiento.isoformat() if l.fecha_vencimiento else None,
        "fabricante": l.fabricante
    } for l in lotes])

@lote_vacuna_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_lote_vacuna_api(id):
    lote = LoteVacuna.query.get_or_404(id)
    return jsonify({
        "id_lote": lote.id_lote,
        "codigo_lote": lote.codigo_lote,
        "fecha_vencimiento": lote.fecha_vencimiento.isoformat() if lote.fecha_vencimiento else None,
        "fabricante": lote.fabricante
    })

@lote_vacuna_bp.route('/api/lotes_vacuna', methods=['POST'])
@token_required
def create_lote_vacuna_api():
    data = request.get_json()
    new_lote = LoteVacuna(
        codigo_lote=data.get('codigo_lote'),
        fecha_vencimiento=datetime.fromisoformat(data.get('fecha_vencimiento')) if data.get('fecha_vencimiento') else None,
        fabricante=data.get('fabricante')
    )
    db.session.add(new_lote)
    db.session.commit()
    return jsonify({"message": "Lote vacuna created", "id": new_lote.id_lote}), 201

@lote_vacuna_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_lote_vacuna_api(id):
    lote = LoteVacuna.query.get_or_404(id)
    data = request.get_json()
    lote.codigo_lote = data.get('codigo_lote', lote.codigo_lote)
    lote.fecha_vencimiento = datetime.fromisoformat(data.get('fecha_vencimiento')) if data.get('fecha_vencimiento') else None
    lote.fabricante = data.get('fabricante', lote.fabricante)
    db.session.commit()
    return jsonify({"message": "Lote vacuna updated"})

@lote_vacuna_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_lote_vacuna_api(id):
    lote = LoteVacuna.query.get_or_404(id)
    db.session.delete(lote)
    db.session.commit()
    return jsonify({"message": "Lote vacuna deleted"})
@lote_vacuna_bp.route('/<int:id>/delete', methods=['GET'])
@login_required
def delete_confirm(id):
    lote = LoteVacuna.query.get_or_404(id)
    return render_template('lote_vacuna/delete.html', lote=lote)

@lote_vacuna_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    try:
        lote = LoteVacuna.query.get_or_404(id)
        db.session.delete(lote)
        db.session.commit()
        flash('Lote de vacuna eliminado exitosamente!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el lote de vacuna: {str(e)}', 'error')
    return redirect(url_for('lote_vacuna.index'))
