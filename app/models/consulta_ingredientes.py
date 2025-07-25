from app import db

class ConsultaIngredientes(db.Model):
    __tablename__ = 'consulta_ingredientes'

    id_consulta = db.Column(db.Integer, db.ForeignKey('consulta_bromatologica.id_consulta'), primary_key=True)
    id_ingrediente = db.Column(db.Integer, db.ForeignKey('ingrediente.id_ingrediente'), primary_key=True)
    resultado = db.Column(db.Text, nullable=True)

    consulta = db.relationship('ConsultaBromatologica', backref='ingredientes')
    ingrediente = db.relationship('Ingrediente', back_populates='consultas')