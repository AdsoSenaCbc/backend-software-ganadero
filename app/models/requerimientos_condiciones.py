from app import db

class RequerimientosCondiciones(db.Model):
    __tablename__ = 'requerimientos_condiciones'

    id_requerimiento = db.Column(db.Integer, db.ForeignKey('requerimientos_nutricionales.id_requerimiento'), primary_key=True)
    id_condicion = db.Column(db.Integer, db.ForeignKey('condiciones_especiales.id_condicion'), primary_key=True)

    requerimiento = db.relationship('RequerimientosNutricionales', backref='condiciones_de_requerimiento')  # Cambiado a nombre único
    condicion = db.relationship('CondicionesEspeciales', backref='requerimientos_condiciones')
    