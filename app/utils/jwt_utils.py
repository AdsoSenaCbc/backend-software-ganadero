import jwt
from flask_jwt_extended import verify_jwt_in_request
from flask import current_app, request, jsonify
from functools import wraps
from datetime import datetime, timedelta

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

def token_required(f):
    """Decorator que valida un JWT emitido por flask_jwt_extended.
    Acepta el token en el header `Authorization: Bearer <token>`.
    Si el token es inválido o está ausente devuelve 401.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()  # Lanza excepción si no es válido o falta
        except Exception as err:
            return jsonify({"message": str(err)}), 401
        return f(*args, **kwargs)
    return decorated