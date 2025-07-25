from app import db

class RolUsuario(db.Model):
    __tablename__ = 'rol_usuario'

    id_rol = db.Column(db.Integer, primary_key=True)
    nombre_rol = db.Column(db.String(50), nullable=False, unique=True)

    # Relación inversa (opcional, ya definida en Usuario)