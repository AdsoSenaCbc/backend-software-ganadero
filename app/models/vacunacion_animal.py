from app import db

class VacunacionAnimal(db.Model):
    __tablename__ = 'vacunacion_animal'

    id_vacunacion = db.Column(db.Integer, primary_key=True)
    id_animal = db.Column(db.Integer, db.ForeignKey('animal.id_animal'), nullable=True)
    id_vacuna = db.Column(db.Integer, db.ForeignKey('vacuna.id_vacuna'), nullable=True)
    id_lote = db.Column(db.Integer, db.ForeignKey('lote_vacuna.id_lote'), nullable=True)
    fecha_aplicacion = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())
    dosis_aplicada = db.Column(db.DECIMAL(6, 2), nullable=True)
    observaciones = db.Column(db.Text, nullable=True)

    # relación inversa generada en Animal mediante backref='vacunaciones'
    vacuna = db.relationship('Vacuna', backref='vacunaciones_animal')  # Mantener nombre existente
    lote = db.relationship('LoteVacuna', backref='vacunaciones_de_lote')