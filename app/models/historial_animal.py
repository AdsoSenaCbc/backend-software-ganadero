from app import db

class HistorialAnimal(db.Model):
    __tablename__ = 'historial_animal'

    id_historial = db.Column(db.Integer, primary_key=True)
    id_animal = db.Column(db.Integer, db.ForeignKey('animal.id_animal'), nullable=True)
    id_hacienda = db.Column(db.Integer, db.ForeignKey('hacienda.id_hacienda'), nullable=True)
    fecha_ingreso = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())
    fecha_salida = db.Column(db.DateTime, nullable=True)
    observaciones = db.Column(db.Text, nullable=True)

    # relación inversa generada en Animal mediante backref='historiales'
    hacienda = db.relationship('Hacienda', backref='historiales_animal')
    