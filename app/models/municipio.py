from app import db

class Municipio(db.Model):
    __tablename__ = 'municipio'

    id_municipio = db.Column(db.Integer, primary_key=True)
    nombre_municipio = db.Column(db.String(100), nullable=False)
    id_departamento = db.Column(db.Integer, db.ForeignKey('departamento.id_departamento'), nullable=True)

    departamento = db.relationship('Departamento', back_populates='municipios')
    haciendas = db.relationship('Hacienda', back_populates='municipio')