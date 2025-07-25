from app import db

class CaracteristicasNutricionales(db.Model):
    __tablename__ = 'caracteristicas_nutricionales'

    id_caracteristica = db.Column(db.Integer, primary_key=True)
    id_ingrediente = db.Column(db.Integer, db.ForeignKey('ingrediente.id_ingrediente'), nullable=True)
    id_nutriente = db.Column(db.Integer, db.ForeignKey('nutrientes.id_nutriente'), nullable=True)
    valor = db.Column(db.DECIMAL(10, 4), nullable=True)

    # relación inversa generada en Ingrediente mediante backref='caracteristicas_nutricionales'
    # relación inversa generada en Nutrientes mediante backref='caracteristicas_nutricionales'