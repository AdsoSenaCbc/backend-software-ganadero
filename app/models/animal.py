from app import db

class Animal(db.Model):
    __tablename__ = 'animal'

    id_animal = db.Column(db.Integer, primary_key=True)
    identificador_unico = db.Column(db.String(50), unique=True, nullable=True)
    nombre = db.Column(db.String(50), nullable=True)

    id_hacienda = db.Column(db.Integer, db.ForeignKey('hacienda.id_hacienda'), nullable=True)
    id_raza = db.Column(db.Integer, db.ForeignKey('raza.id_raza'), nullable=True)
    id_sexo = db.Column(db.Integer, db.ForeignKey('sexo.id_sexo'), nullable=True)
    id_especie = db.Column(db.Integer, db.ForeignKey('especie.id_especie'), nullable=True)
    id_estado = db.Column(db.Integer, db.ForeignKey('estado_animal.id_estado'), nullable=True)
    id_etapa = db.Column(db.Integer, db.ForeignKey('etapas_productivas.id_etapa'), nullable=True)

    # En la base de datos la columna se llama 'peso'. Renombramos en el modelo
    peso = db.Column(db.DECIMAL(6, 2), nullable=True)

    observaciones = db.Column(db.Text, nullable=True)

    # Alias de compatibilidad para el código que todavía usa 'peso_actual'
    @property
    def peso_actual(self):
        return self.peso

    @peso_actual.setter
    def peso_actual(self, value):
        self.peso = value

    hacienda = db.relationship('Hacienda', backref='animals')
    raza = db.relationship('Raza', backref='animales')
    sexo = db.relationship('Sexo', backref='animales')
    especie = db.relationship('Especie', backref='animales')
    estado = db.relationship('EstadoAnimal', backref='animales')
    eventos = db.relationship('EventoAnimal', backref='animal')
    historiales = db.relationship('HistorialAnimal', backref='animal')
    nacimientos_cria = db.relationship('Nacimiento', foreign_keys='Nacimiento.id_cria', backref='cria')
    nacimientos_madre = db.relationship('Nacimiento', foreign_keys='Nacimiento.id_madre', backref='madre')
    nacimientos_padre = db.relationship('Nacimiento', foreign_keys='Nacimiento.id_padre', backref='padre')
    raciones = db.relationship('Racion', backref='animal')
    vacunaciones = db.relationship('VacunacionAnimal', backref='animal')