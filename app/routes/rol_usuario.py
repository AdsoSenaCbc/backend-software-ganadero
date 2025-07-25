from flask import Blueprint, request, jsonify
from app import db
from app.models.rol_usuario import RolUsuario
from app.utils.jwt_utils import token_required

rol_usuario_bp = Blueprint('rol_usuario', __name__)

@rol_usuario_bp.route('/', methods=['GET'])
@token_required
def get_roles_usuario():
    roles = RolUsuario.query.all()
    return jsonify([{
        "id_rol": r.id_rol,
        "nombre_rol": r.nombre_rol
    } for r in roles])

@rol_usuario_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_rol_usuario(id):
    rol = RolUsuario.query.get_or_404(id)
    return jsonify({
        "id_rol": rol.id_rol,
        "nombre_rol": rol.nombre_rol
    })

@rol_usuario_bp.route('/', methods=['POST'])
@token_required
def create_rol_usuario():
    data = request.get_json()
    new_rol = RolUsuario(
        nombre_rol=data.get('nombre_rol')
    )
    db.session.add(new_rol)
    db.session.commit()
    return jsonify({"message": "Rol usuario created", "id": new_rol.id_rol}), 201

@rol_usuario_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_rol_usuario(id):
    rol = RolUsuario.query.get_or_404(id)
    data = request.get_json()
    rol.nombre_rol = data.get('nombre_rol', rol.nombre_rol)
    db.session.commit()
    return jsonify({"message": "Rol usuario updated"})

@rol_usuario_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_rol_usuario(id):
    rol = RolUsuario.query.get_or_404(id)
    db.session.delete(rol)
    db.session.commit()
    return jsonify({"message": "Rol usuario deleted"})