from app import db

class EstadoAnimal(db.Model):
    __tablename__ = 'estado_animal'

    id_estado = db.Column(db.Integer, primary_key=True)
    nombre_estado = db.Column(db.String(50), nullable=False)

    # relación inversa generada en Animal