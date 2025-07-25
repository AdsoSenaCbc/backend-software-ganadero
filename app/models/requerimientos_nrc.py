from app import db

class RequerimientosNrc(db.Model):
    __tablename__ = 'requerimientos_nrc'

    id = db.Column(db.Integer, primary_key=True)
    etapa = db.Column(db.String(50), nullable=False)
    peso = db.Column(db.DECIMAL(6, 2), nullable=True)
    produccion_leche = db.Column(db.DECIMAL(6, 2), nullable=True)
    grasa_leche = db.Column(db.DECIMAL(6, 2), nullable=True)
    em = db.Column(db.DECIMAL(10, 4), nullable=True)
    pc = db.Column(db.DECIMAL(10, 4), nullable=True)
    ms = db.Column(db.DECIMAL(10, 2), nullable=True)
    observaciones = db.Column(db.Text, nullable=True)