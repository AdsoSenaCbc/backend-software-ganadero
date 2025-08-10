from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app import db
from app.models.usuario import Usuario
from app.utils.jwt_utils import token_required
from flask_login import login_required

user_bp = Blueprint('user', __name__)

# --------------------------
# API JSON ENDPOINTS
# --------------------------
@user_bp.route('/api', methods=['GET'])
@token_required
def get_users_api():
    users = Usuario.query.all()
    return jsonify([
        {
            "id_usuario": u.id_usuario,
            "nombres": u.nombres,
            "apellidos": u.apellidos
        } for u in users
    ])

@user_bp.route('/', methods=['GET'])
@token_required
def list_users_public():
    return get_users_api()

# Endpoint específico para el frontend React
@user_bp.route('/list', methods=['GET'])
@token_required
def api_list_users():
    return get_users_api()

# --------------------------
# HTML FORM ROUTES
# --------------------------
@user_bp.route('/', methods=['GET'])
@login_required
def index():
    users = Usuario.query.all()
    return render_template('user/index.html', users=users)

@user_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_user_form():
    if request.method == 'POST':
        nombres = request.form.get('nombres')
        apellidos = request.form.get('apellidos')
        documento = request.form.get('documento')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono')
        contrasena = request.form.get('contrasena')
        id_rol = request.form.get('id_rol')
        if not (nombres and apellidos and documento and correo and contrasena):
            flash('Todos los campos obligatorios deben completarse', 'danger')
            return redirect(url_for('user.create_user_form'))
        nuevo = Usuario(nombres=nombres, apellidos=apellidos, documento=documento, correo=correo,
                        telefono=telefono, contrasena=contrasena, id_rol=id_rol)
        db.session.add(nuevo)
        db.session.commit()
        flash('Usuario creado correctamente.', 'success')
        return redirect(url_for('user.index'))
    return render_template('user/create.html')

@user_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_user_form(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        usuario.nombres = request.form.get('nombres', usuario.nombres)
        usuario.apellidos = request.form.get('apellidos', usuario.apellidos)
        usuario.documento = request.form.get('documento', usuario.documento)
        usuario.correo = request.form.get('correo', usuario.correo)
        usuario.telefono = request.form.get('telefono', usuario.telefono)
        usuario.id_rol = request.form.get('id_rol', usuario.id_rol)
        db.session.commit()
        flash('Usuario actualizado correctamente.', 'success')
        return redirect(url_for('user.index'))
    return render_template('user/update.html', user=usuario)

@user_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_user_form(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuario eliminado correctamente.', 'success')
        return redirect(url_for('user.index'))
    return render_template('user/delete.html', user=usuario)

# --------------------------
# API JSON ENDPOINTS
# --------------------------
@user_bp.route('/api', methods=['GET'])
@token_required
def get_users_api():
    users = Usuario.query.all()
    return jsonify([{
        "id_usuario": u.id_usuario,
        "nombres": u.nombres,
        "apellidos": u.apellidos,
        "documento": u.documento,
        "correo": u.correo,
        "telefono": u.telefono,
        "fecha_creacion": u.fecha_creacion.isoformat(),
        "fecha_modificacion": u.fecha_modificacion.isoformat() if u.fecha_modificacion else None,
        "usuario_modifico": u.usuario_modifico,
        "id_rol": u.id_rol
    } for u in users])

@user_bp.route('/api/<int:id>', methods=['GET'])
@token_required
def get_user_api(id):
    user = Usuario.query.get_or_404(id)
    return jsonify({
        "id_usuario": user.id_usuario,
        "nombres": user.nombres,
        "apellidos": user.apellidos,
        "documento": user.documento,
        "correo": user.correo,
        "telefono": user.telefono,
        "fecha_creacion": user.fecha_creacion.isoformat(),
        "fecha_modificacion": user.fecha_modificacion.isoformat() if user.fecha_modificacion else None,
        "usuario_modifico": user.usuario_modifico,
        "id_rol": user.id_rol
    })

@user_bp.route('/api', methods=['POST'])
@token_required
def create_user_api():
    data = request.get_json()
    new_user = Usuario(
        nombres=data.get('nombres'),
        apellidos=data.get('apellidos'),
        documento=data.get('documento'),
        correo=data.get('correo'),
        telefono=data.get('telefono'),
        id_rol=data.get('id_rol')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Usuario created", "id": new_user.id_usuario}), 201

@user_bp.route('/api/<int:id>', methods=['PUT'])
@token_required
def update_user_api(id):
    user = Usuario.query.get_or_404(id)
    data = request.get_json()
    user.nombres = data.get('nombres', user.nombres)
    user.apellidos = data.get('apellidos', user.apellidos)
    user.documento = data.get('documento', user.documento)
    user.correo = data.get('correo', user.correo)
    user.telefono = data.get('telefono', user.telefono)
    user.usuario_modifico = data.get('usuario_modifico', user.usuario_modifico)
    user.id_rol = data.get('id_rol', user.id_rol)
    db.session.commit()
    return jsonify({"message": "Usuario updated"})

@user_bp.route('/api/<int:id>', methods=['DELETE'])
@token_required
def delete_user_api(id):
    user = Usuario.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Usuario deleted"})