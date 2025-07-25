from app import db

class Departamento(db.Model):
    __tablename__ = 'departamento'

    id_departamento = db.Column(db.Integer, primary_key=True)
    nombre_departamento = db.Column(db.String(100), nullable=False)

    municipios = db.relationship('Municipio', back_populates='departamento')
    haciendas = db.relationship('Hacienda', back_populates='departamento')