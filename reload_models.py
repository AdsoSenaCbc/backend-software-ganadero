from app import create_app, db
from app.models.vacuna import Vacuna

app = create_app()

with app.app_context():
    # Forzar la recarga de los modelos
    from sqlalchemy import inspect
    
    # Eliminar la tabla de la caché de metadatos
    if 'vacuna' in db.metadata.tables:
        db.metadata.remove(db.metadata.tables['vacuna'])
    
    # Eliminar el mapeo de la clase Vacuna
    if hasattr(Vacuna, '__mapper__'):
        from sqlalchemy.orm import class_mapper
        try:
            class_mapper(Vacuna).dispose()
        except:
            pass
    
    # Recargar el modelo
    import importlib
    import sys
    
    if 'app.models.vacuna' in sys.modules:
        importlib.reload(sys.modules['app.models.vacuna'])
    
    # Recrear el mapeo
    from sqlalchemy import Table
    from sqlalchemy.ext.declarative import declarative_base
    
    Base = declarative_base()
    Base.metadata = db.metadata
    
    # Definir el modelo nuevamente
    class VacunaReloaded(db.Model):
        __tablename__ = 'vacuna'
        
        id_vacuna = db.Column(db.Integer, primary_key=True)
        nombre = db.Column(db.String(100), nullable=False)
        descripcion = db.Column(db.Text, nullable=True)
        dosis_recomendada = db.Column(db.DECIMAL(6, 2), nullable=True)
        
        vacunaciones = db.relationship('VacunacionAnimal', backref='vacuna_de_vacunacion')
    
    # Actualizar la referencia en el módulo
    import app.models.vacuna as vacuna_module
    vacuna_module.Vacuna = VacunaReloaded
    
    # Verificar la estructura
    print("Estructura de la tabla después de la recarga:")
    print("-" * 50)
    
    inspector = db.inspect(db.engine)
    columns = inspector.get_columns('vacuna')
    
    print("Columnas en la base de datos:")
    for column in columns:
        print(f"- {column['name']}: {column['type']}")
    
    print("\nModelo Vacuna después de la recarga:")
    print(f"- id_vacuna: {VacunaReloaded.id_vacuna}")
    print(f"- nombre: {VacunaReloaded.nombre}")
    print(f"- descripcion: {VacunaReloaded.descripcion}")
    print(f"- dosis_recomendada: {VacunaReloaded.dosis_recomendada}")
    
    print("\nPrueba de consulta:")
    try:
        vacunas = VacunaReloaded.query.limit(5).all()
        print(f"Se encontraron {len(vacunas)} vacunas")
        for v in vacunas:
            print(f"- {v.nombre}")
    except Exception as e:
        print(f"Error al consultar: {str(e)}")
