from app import db

class IngredienteMateriaPrima(db.Model):
    __tablename__ = 'ingrediente_materia_prima'

    id_ingrediente = db.Column(db.Integer, db.ForeignKey('ingrediente.id_ingrediente'), primary_key=True)
    id_materia = db.Column(db.Integer, db.ForeignKey('materia_prima.id_materia'), primary_key=True)
    cantidad_kg = db.Column(db.DECIMAL(10, 2), nullable=True)

    ingrediente = db.relationship(
        'Ingrediente',
        back_populates='relaciones_materia',
        overlaps="ingredientes,relaciones_materia"
    )
    materia_prima = db.relationship(
        'MateriaPrima',
        backref='ingredientes_de_materia',
        overlaps="ingredientes,relaciones_materia"
    )  # Cambiado a nombre único