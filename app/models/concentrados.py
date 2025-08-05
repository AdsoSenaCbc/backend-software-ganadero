from app import db
from datetime import datetime

class Concentrados(db.Model):
    __tablename__ = 'concentrados'

    id_concentrado = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Ejemplo: "Proteico", "Energético"
    descripcion = db.Column(db.Text)
    costo_kg = db.Column(db.Numeric(10, 2))





    def __repr__(self):
        return f'<Concentrados {self.nombre}>'