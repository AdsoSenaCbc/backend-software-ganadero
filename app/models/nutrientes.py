from app import db

class Nutrientes(db.Model):
    __tablename__ = 'nutrientes'

    id_nutriente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    unidad = db.Column(db.String(20), nullable=True)

    caracteristicas_nutricionales = db.relationship('CaracteristicasNutricionales', backref='nutriente')
    detalles_racion_nutricionales = db.relationship('DetalleRacionNutricional', back_populates='nutriente')
    requerimientos_nutricionales = db.relationship('RequerimientosNutricionales', backref='nutriente_de_requerimiento')  # Cambiado a nombre único