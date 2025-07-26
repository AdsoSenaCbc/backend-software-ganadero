from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.rol_usuario import RolUsuario
from app.utils.jwt_utils import token_required
from flask_login import login_required

rol_usuario_bp = Blueprint('rol_usuario', __name__)

# --------------------------
# HTML FORM ROUTES
# --------------------------
@rol_usuario_bp.route('/', methods=['GET'])
@login_required
def index():
    roles = RolUsuario.query.all()
    return render_template('rol_usuario/index.html', roles=roles)

@rol_usuario_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_rol():
    if request.method == 'POST':
        nombre = request.form.get('nombre_rol')
        if not nombre:
            flash('El nombre del rol es requerido', 'danger')
            return redirect(url_for('rol_usuario.create_rol'))
        nuevo = RolUsuario(nombre_rol=nombre)
        db.session.add(nuevo)
        db.session.commit()
        flash('Rol creado correctamente.', 'success')
        return redirect(url_for('rol_usuario.index'))
    return render_template('rol_usuario/create.html')

@rol_usuario_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_rol(id):
    rol = RolUsuario.query.get_or_404(id)
    if request.method == 'POST':
        rol.nombre_rol = request.form.get('nombre_rol', rol.nombre_rol)
        db.session.commit()
        flash('Rol actualizado correctamente.', 'success')
        return redirect(url_for('rol_usuario.index'))
    return render_template('rol_usuario/update.html', rol=rol)

@rol_usuario_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_rol(id):
    rol = RolUsuario.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(rol)
        db.session.commit()
        flash('Rol eliminado correctamente.', 'success')
        return redirect(url_for('rol_usuario.index'))
    return render_template('rol_usuario/delete.html', rol=rol)

# --------------------------
# API JSON ENDPOINTS
# --------------------------
@rol_usuario_bp.route('/api', methods=['GET'])
@token_required
def get_roles_api():
    roles = RolUsuario.query.all()
    return jsonify([{
        "id_rol": r.id_rol,
        "nombre_rol": r.nombre_rol
    } for r in roles])

@rol_usuario_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_rol_api(id):
    rol = RolUsuario.query.get_or_404(id)
    return jsonify({
        "id_rol": rol.id_rol,
        "nombre_rol": rol.nombre_rol
    })

@rol_usuario_bp.route('/api', methods=['POST'])
@token_required
def create_rol_api():
    data = request.get_json()
    new_rol = RolUsuario(
        nombre_rol=data.get('nombre_rol')
    )
    db.session.add(new_rol)
    db.session.commit()
    return jsonify({"message": "Rol usuario created", "id": new_rol.id_rol}), 201

@rol_usuario_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_rol_api(id):
    rol = RolUsuario.query.get_or_404(id)
    data = request.get_json()
    rol.nombre_rol = data.get('nombre_rol', rol.nombre_rol)
    db.session.commit()
    return jsonify({"message": "Rol usuario updated"})

@rol_usuario_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_rol_api(id):
    rol = RolUsuario.query.get_or_404(id)
    db.session.delete(rol)
    db.session.commit()
    return jsonify({"message": "Rol usuario deleted"})