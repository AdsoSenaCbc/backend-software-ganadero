from app import db

class Raza(db.Model):
    __tablename__ = 'raza'

    id_raza = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    # Relación inversa generada en Animal mediante backref='animals'