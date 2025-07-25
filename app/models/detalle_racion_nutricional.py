from app import db

class DetalleRacionNutricional(db.Model):
    __tablename__ = 'detalle_racion_nutricional'

    id_detalle_nut = db.Column(db.Integer, primary_key=True)
    id_racion = db.Column(db.Integer, db.ForeignKey('racion.id_racion'), nullable=True)
    id_nutriente = db.Column(db.Integer, db.ForeignKey('nutrientes.id_nutriente'), nullable=True)
    valor_aportado = db.Column(db.DECIMAL(10, 4), nullable=True)

    racion = db.relationship('Racion', back_populates='detalles_nutricionales')
    nutriente = db.relationship('Nutrientes', back_populates='detalles_racion_nutricionales')