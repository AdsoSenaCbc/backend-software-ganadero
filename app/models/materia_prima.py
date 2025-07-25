from app import db

class MateriaPrima(db.Model):
    __tablename__ = 'materia_prima'

    id_materia = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fuente = db.Column(db.String(50), nullable=True)
    descripcion = db.Column(db.Text, nullable=True)

    ingredientes = db.relationship(
        'IngredienteMateriaPrima',
        backref='materia_prima_de_ingrediente',
        overlaps="ingrediente,materia_prima"
    )  # Ajustado para consistencia