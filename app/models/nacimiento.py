from app import db

class Nacimiento(db.Model):
    __tablename__ = 'nacimiento'

    id_nacimiento = db.Column(db.Integer, primary_key=True)
    id_cria = db.Column(db.Integer, db.ForeignKey('animal.id_animal'), nullable=True)
    id_madre = db.Column(db.Integer, db.ForeignKey('animal.id_animal'), nullable=True)
    id_padre = db.Column(db.Integer, db.ForeignKey('animal.id_animal'), nullable=True)
    fecha_nacimiento = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())
    peso_nacimiento = db.Column(db.DECIMAL(6, 2), nullable=True)
    tipo_parto = db.Column(db.String(50), nullable=True)
    complicaciones = db.Column(db.Text, nullable=True)
    observaciones = db.Column(db.Text, nullable=True)

    # relación inversa generada en Animal mediante backref='cria'
    # relación inversa generada en Animal mediante backref='madre'
    # relación inversa generada en Animal mediante backref='padre'