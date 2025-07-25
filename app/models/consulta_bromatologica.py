from app import db

class ConsultaBromatologica(db.Model):
    __tablename__ = 'consulta_bromatologica'

    id_consulta = db.Column(db.Integer, primary_key=True)
    fecha_consulta = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=True)

    usuario = db.relationship('Usuario', backref='consultas_bromatologicas')