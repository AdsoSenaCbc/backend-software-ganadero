from app import db

class LoteVacuna(db.Model):
    __tablename__ = 'lote_vacuna'

    id_lote = db.Column(db.Integer, primary_key=True)
    codigo_lote = db.Column(db.String(50), nullable=False)
    fecha_vencimiento = db.Column(db.DateTime, nullable=True)
    fabricante = db.Column(db.String(100), nullable=True)

    vacunaciones = db.relationship('VacunacionAnimal', backref='lote_de_vacunacion')  # Cambiado a nombre único