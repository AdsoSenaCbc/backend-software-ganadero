from app import db

class Hacienda(db.Model):
    __tablename__ = 'hacienda'
    id_hacienda = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tel_contacto = db.Column(db.String(30))
    ubicacion = db.Column(db.Text)
    descripcion = db.Column(db.Text)
    id_departamento = db.Column(db.Integer, db.ForeignKey('departamento.id_departamento'))
    id_municipio = db.Column(db.Integer, db.ForeignKey('municipio.id_municipio'))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))

    departamento = db.relationship('Departamento', back_populates='haciendas')
    municipio = db.relationship('Municipio', back_populates='haciendas')
    usuario = db.relationship('Usuario', backref='haciendas')
    # Relación con Concentrados
  # Corregí 'User' a 'Usuario' para que coincida con el modelo