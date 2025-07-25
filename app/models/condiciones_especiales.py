from app import db

class CondicionesEspeciales(db.Model):
    __tablename__ = 'condiciones_especiales'

    id_condicion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    ajuste_nutriente = db.Column(db.DECIMAL(10, 4), nullable=True)