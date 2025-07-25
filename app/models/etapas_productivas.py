from app import db

class EtapasProductivas(db.Model):
    __tablename__ = 'etapas_productivas'

    id_etapa = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)

    animals = db.relationship('Animal', backref='etapa')
    requerimientos = db.relationship('RequerimientosNutricionales', back_populates='etapa')