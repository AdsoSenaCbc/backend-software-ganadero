from app import db

class TipoEvento(db.Model):
    __tablename__ = 'tipo_evento'

    id_tipo_evento = db.Column(db.Integer, primary_key=True)
    nombre_tipo = db.Column(db.String(50), nullable=False)

    eventos_animal = db.relationship('EventoAnimal', back_populates='tipo_evento')