from app import db

class Vacuna(db.Model):
    __tablename__ = 'vacuna'

    id_vacuna = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    dosis_recomendada = db.Column(db.DECIMAL(6, 2), nullable=True)

    vacunaciones = db.relationship('VacunacionAnimal', backref='vacuna_de_vacunacion')  # Cambiado a nombre único