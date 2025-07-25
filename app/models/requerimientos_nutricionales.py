from app import db

class RequerimientosNutricionales(db.Model):
    __tablename__ = 'requerimientos_nutricionales'

    id_requerimiento = db.Column(db.Integer, primary_key=True)
    id_etapa = db.Column(db.Integer, db.ForeignKey('etapas_productivas.id_etapa'), nullable=True)
    peso_min = db.Column(db.DECIMAL(6, 2), nullable=True)
    peso_max = db.Column(db.DECIMAL(6, 2), nullable=True)
    id_nutriente = db.Column(db.Integer, db.ForeignKey('nutrientes.id_nutriente'), nullable=True)
    valor_min = db.Column(db.DECIMAL(10, 4), nullable=True)
    valor_max = db.Column(db.DECIMAL(10, 4), nullable=True)
    condicion = db.Column(db.String(50), nullable=True)

    etapa = db.relationship('EtapasProductivas', back_populates='requerimientos')
    nutriente = db.relationship('Nutrientes', backref='requerimientos_de_nutriente')
    raciones = db.relationship('Racion', backref='requerimiento_de_racion')
    condiciones = db.relationship('RequerimientosCondiciones', backref='requerimiento_nutricional')  # Mantener nombre único