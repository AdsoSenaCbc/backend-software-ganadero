from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import BadRequest
from app import db
from app.models.usuario import Usuario

api_auth_bp = Blueprint("api_auth", __name__, url_prefix="/api/auth")

# ------------------------------
# Helpers
# ------------------------------

def _usuario_to_dict(usuario: Usuario) -> dict:
    """Serialize Usuario instance to dict (only safe, needed fields)."""
    return {
        "id_usuario": usuario.id_usuario,
        "nombres": usuario.nombres,
        "apellidos": usuario.apellidos,
        "documento": usuario.documento,
        "correo": usuario.correo,
        "telefono": usuario.telefono,
        "id_rol": usuario.id_rol,
    }

# ------------------------------
# Register (English)
# ------------------------------

@api_auth_bp.route("/register", methods=["POST"])
def api_register():
    data = request.get_json()
    if not data:
        raise BadRequest("JSON body required")

    required = [
        "nombres",
        "apellidos",
        "documento",
        "correo",
        "telefono",
        "password",
        "id_rol",
    ]
    missing = [field for field in required if not data.get(field)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    if Usuario.query.filter_by(correo=data["correo"]).first():
        return jsonify({"error": "Correo ya registrado"}), 409

    nuevo = Usuario(
        nombres=data["nombres"],
        apellidos=data["apellidos"],
        documento=data["documento"],
        correo=data["correo"],
        telefono=data["telefono"],
        id_rol=int(data["id_rol"]),
    )
    nuevo.password = data["password"]  # hashed via property setter
    db.session.add(nuevo)
    db.session.commit()

    return jsonify({"message": "Usuario creado", "id_usuario": nuevo.id_usuario, "usuario": _usuario_to_dict(nuevo)}), 201

# ------------------------------
# Registrar (Spanish alias used by React frontend)
# ------------------------------

@api_auth_bp.route("/registrar", methods=["POST"])  # matches /api/auth/registrar
def api_registrar():
    """Alias que acepta campos en español/snake usados por el frontend React."""
    data = request.get_json() or {}

    # Mapeo de nombres provenientes del front
    payload = {
        "nombres": data.get("nombres"),
        "apellidos": data.get("apellidos"),
        "documento": data.get("documento"),
        "correo": data.get("email") or data.get("correo"),
        "telefono": data.get("telefono", ""),
        "password": data.get("password"),
        "id_rol": data.get("rol") or data.get("id_rol", 2),
    }

    # Validación rápida
    missing = [k for k, v in payload.items() if k in ["nombres", "apellidos", "correo", "password"] and not v]
    if missing:
        return jsonify({"error": f"Faltan campos requeridos: {', '.join(missing)}"}), 400

    if Usuario.query.filter_by(correo=payload["correo"]).first():
        return jsonify({"error": "Correo ya registrado"}), 409

    nuevo = Usuario(
        nombres=payload["nombres"],
        apellidos=payload["apellidos"],
        documento=payload["documento"],
        correo=payload["correo"],
        telefono=payload["telefono"],
        id_rol=(
            int(payload["id_rol"]) if str(payload["id_rol"]).isdigit() else {
                "Aprendiz": 1,
                "Instructor": 2,
            }.get(payload["id_rol"], 2)
        ),
    )
    nuevo.password = payload["password"]
    db.session.add(nuevo)
    db.session.commit()

    return jsonify({"message": "Usuario creado", "usuario": _usuario_to_dict(nuevo)}), 201

# ------------------------------
# Login
# ------------------------------

@api_auth_bp.route("/login", methods=["POST"])
def api_login():
    data = request.get_json()
    if not data:
        raise BadRequest("JSON body required")

    correo = data.get("email") or data.get("correo")
    password = data.get("password")
    if not correo or not password:
        return jsonify({"error": "Correo y password son obligatorios"}), 400

    user = Usuario.query.filter_by(correo=correo).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    rol_map = {1: "Aprendiz", 2: "Instructor"}
    role_str = rol_map.get(user.id_rol, "Aprendiz")
    access_token = create_access_token(identity={"id_usuario": user.id_usuario, "rol": role_str, "email": user.correo})

    return jsonify({"access_token": access_token, "usuario": {**_usuario_to_dict(user), "rol": role_str}}), 200

# ------------------------------
# Forgot Password (stub)
# ------------------------------

@api_auth_bp.route("/forgot-password", methods=["POST"])
def api_forgot_password():
    data = request.get_json() or {}
    correo = data.get("correo")
    if not correo:
        return jsonify({"error": "Correo requerido"}), 400

    # TODO: Implement email sending with token link.
    # Por ahora devolvemos éxito simulado.
    return jsonify({"message": "Si el correo existe, se ha enviado un enlace de recuperación"}), 200
