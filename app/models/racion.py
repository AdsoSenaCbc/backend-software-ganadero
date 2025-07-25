from app import db

class Racion(db.Model):
    __tablename__ = 'racion'

    id_racion = db.Column(db.Integer, primary_key=True)
    id_animal = db.Column(db.Integer, db.ForeignKey('animal.id_animal'), nullable=True)
    id_requerimiento = db.Column(db.Integer, db.ForeignKey('requerimientos_nutricionales.id_requerimiento'), nullable=True)
    fecha_calculo = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())
    ms_total = db.Column(db.DECIMAL(10, 2), nullable=True)
    calculado_por = db.Column(db.String(50), nullable=True)
    observaciones = db.Column(db.Text, nullable=True)

    # relación inversa generada en Animal mediante backref='raciones'
    requerimiento = db.relationship('RequerimientosNutricionales', backref='raciones_de_requerimiento')
    detalles = db.relationship('DetalleRacion', backref='racion_de_detalle')
    detalles_nutricionales = db.relationship('DetalleRacionNutricional', back_populates='racion')