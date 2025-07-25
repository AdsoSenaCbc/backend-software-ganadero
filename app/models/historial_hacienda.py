from app import db

class HistorialHacienda(db.Model):
    __tablename__ = 'historial_hacienda'

    id_historial = db.Column(db.Integer, primary_key=True)
    id_hacienda = db.Column(db.Integer, db.ForeignKey('hacienda.id_hacienda'), nullable=True)
    fecha = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())
    existencia_animales = db.Column(db.DECIMAL(10, 2), nullable=True)
    area = db.Column(db.DECIMAL(10, 2), nullable=True)
    estado = db.Column(db.String(50), nullable=True)
    observaciones = db.Column(db.Text, nullable=True)

    hacienda = db.relationship('Hacienda', backref='historiales_hacienda')