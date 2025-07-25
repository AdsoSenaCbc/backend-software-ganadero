from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    __table_args__ = {'extend_existing': True}

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    documento = db.Column(db.String(20), unique=True, nullable=False, info={'constraint_name': 'uq_usuario_documento'})
    correo = db.Column(db.String(120), unique=True, nullable=False, info={'constraint_name': 'uq_usuario_correo'})
    telefono = db.Column(db.String(20), nullable=False)
    password_hash = db.Column('contraseña', db.String(256), nullable=False)
    id_rol = db.Column(db.Integer, db.ForeignKey('rol_usuario.id_rol', name='fk_usuario_rol'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, onupdate=datetime.utcnow)
    usuario_modifico = db.Column(db.String(120))

    rol = db.relationship('RolUsuario', backref='usuarios')

    # API de contraseña legible: atributo write-only 'password'
    @property
    def password(self):
        raise AttributeError("password is write-only")

    @password.setter
    def password(self, plain_password):
        if not plain_password:
            raise ValueError("La contraseña no puede ir vacía")
        self.password_hash = generate_password_hash(plain_password, method='pbkdf2:sha256', salt_length=16)



    def check_password(self, plain_password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, plain_password)

    # Flask-Login compatibility
    def get_id(self):
        """Return the primary key as a string for Flask-Login."""
        return str(self.id_usuario)