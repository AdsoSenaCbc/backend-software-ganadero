from app import db

class Ingrediente(db.Model):
    __tablename__ = 'ingrediente'

    id_ingrediente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=True)
    descripcion = db.Column(db.Text, nullable=True)
    costo_kg = db.Column(db.DECIMAL(10, 2), nullable=True)

    caracteristicas_nutricionales = db.relationship('CaracteristicasNutricionales', backref='ingrediente')
    # Evitar advertencia de overlaps por backref adicional en DetalleRacion
    detalles_racion = db.relationship(
        'DetalleRacion',
        back_populates='ingrediente',
        overlaps="detalles_racion_de_ingrediente,ingrediente"
    )
    consultas = db.relationship('ConsultaIngredientes', back_populates='ingrediente')
    relaciones_materia = db.relationship('IngredienteMateriaPrima', back_populates='ingrediente')