from app import create_app, db
from app.models.vacuna import Vacuna

app = create_app()

with app.app_context():
    # Verificar la estructura de la tabla
    print("Estructura de la tabla vacuna:")
    print("-" * 50)
    
    # Obtener la estructura de la tabla desde la base de datos
    inspector = db.inspect(db.engine)
    columns = inspector.get_columns('vacuna')
    
    print("Columnas en la base de datos:")
    for column in columns:
        print(f"- {column['name']}: {column['type']}")
    
    print("\nModelo Vacuna:")
    print(f"- id_vacuna: {Vacuna.id_vacuna}")
    print(f"- nombre: {Vacuna.nombre}")
    print(f"- descripcion: {Vacuna.descripcion}")
    print(f"- dosis_recomendada: {Vacuna.dosis_recomendada}")
    
    # Verificar si hay alguna relación que pueda estar causando problemas
    print("\nRelaciones:")
    for rel in Vacuna.__mapper__.relationships:
        print(f"- {rel.key} -> {rel.mapper.class_.__name__}")
    
    # Verificar si hay alguna caché de SQLAlchemy
    print("\nMetadata de la tabla:")
    print(Vacuna.__table__.c.keys())
