from app import db
from datetime import datetime

class SalesMinerales(db.Model):
    __tablename__ = 'sales_minerales'

    id_sale_mineral = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    composicion = db.Column(db.String(100))
    contenido_principal = db.Column(db.Numeric(5,2))
    uso_principal = db.Column(db.String(200))
    costo_kg = db.Column(db.Numeric(10,2))


    def __repr__(self):
        return f'<SalesMinerales {self.nombre}>'