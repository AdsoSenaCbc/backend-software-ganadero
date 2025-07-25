from app import db

class EventoAnimal(db.Model):
    __tablename__ = 'evento_animal'

    id_animal = db.Column(db.Integer, db.ForeignKey('animal.id_animal'), primary_key=True)
    id_evento = db.Column(db.Integer, primary_key=True)
    id_tipo_evento = db.Column(db.Integer, db.ForeignKey('tipo_evento.id_tipo_evento'), nullable=True)
    fecha_evento = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())
    valor = db.Column(db.DECIMAL(6, 2), nullable=True)
    observaciones = db.Column(db.Text, nullable=True)

    # relación inversa generada en Animal mediante backref='eventos'
    tipo_evento = db.relationship('TipoEvento', back_populates='eventos_animal')