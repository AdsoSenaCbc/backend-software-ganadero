from flask import Blueprint, request, jsonify
from app import db
from app.models.usuario import Usuario
from app.utils.jwt_utils import token_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
@token_required
def get_users():
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

@user_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_user(id):
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

@user_bp.route('/', methods=['POST'])
@token_required
def create_user():
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

@user_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_user(id):
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

@user_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_user(id):
    user = Usuario.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Usuario deleted"})