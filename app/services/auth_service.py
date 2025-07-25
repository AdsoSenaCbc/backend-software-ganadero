from app import db
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash, check_password_hash

def register_user(data):
    try:
        existing_user = Usuario.query.filter_by(correo=data['correo']).first()
        if existing_user:
            return {"message": "Email already registered"}, 400
        
        new_user = Usuario(
            nombres=data['nombres'],
            apellidos=data['apellidos'],
            correo=data['correo'],
            password=data['password'],
            id_rol=data.get('id_rol',2)
        )
        new_user.password = data['password']
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User registered successfully", "id": new_user.id_usuario}, 201
    except Exception as e:
        db.session.rollback()
        return {"message": str(e)}, 500

def login_user(data):
    try:
        user = Usuario.query.filter_by(correo=data['correo']).first()
        if user and user.check_password(data['password']):
            return user
        return None
    except Exception as e:
        return None