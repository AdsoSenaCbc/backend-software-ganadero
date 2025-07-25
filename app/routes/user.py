from flask import Blueprint, jsonify, request

# BluePrint de usuario mínimo para evitar errores de importación
# Puedes ampliar las rutas según necesidades futuras.
user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
def list_users():
    """Ruta temporal que simplemente devuelve un mensaje de placeholder."""
    return jsonify({'message': 'Endpoint de usuarios en construcción'}), 200
