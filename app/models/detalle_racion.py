from app import db

class DetalleRacion(db.Model):
    __tablename__ = 'detalle_racion'

    id_detalle = db.Column(db.Integer, primary_key=True)
    id_racion = db.Column(db.Integer, db.ForeignKey('racion.id_racion'), nullable=True)
    id_ingrediente = db.Column(db.Integer, db.ForeignKey('ingrediente.id_ingrediente'), nullable=True)
    cantidad_kg = db.Column(db.DECIMAL(10, 2), nullable=True)
    porcentaje_ms = db.Column(db.DECIMAL(10, 2), nullable=True)

    racion = db.relationship(
        'Racion',
        backref='detalles_de_racion',
        overlaps="detalles,racion"
    )  # Mantener consistente
    ingrediente = db.relationship(
        'Ingrediente',
        backref='detalles_racion_de_ingrediente',
        overlaps="detalles_racion,ingrediente"
    )