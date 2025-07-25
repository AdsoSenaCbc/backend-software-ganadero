from app import db

class Sexo(db.Model):
    __tablename__ = 'sexo'

    id_sexo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)

    # Relación inversa generada en Animal mediante backref='animals'