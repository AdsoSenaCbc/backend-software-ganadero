from sqlalchemy import create_engine, inspect, text

# Configura la conexión a la base de datos
db_uri = 'mysql+pymysql://root:@localhost/sistema_ganadero_database'
engine = create_engine(db_uri)

# Verifica la estructura de la tabla
inspector = inspect(engine)
print("Tablas en la base de datos:", inspector.get_table_names())

# Verifica las columnas de la tabla vacuna
print("\nColumnas en la tabla 'vacuna':")
columns = inspector.get_columns('vacuna')
for column in columns:
    print(f"- {column['name']}: {column['type']}")

# Intenta hacer una consulta directa
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM vacuna LIMIT 1"))
        print("\nPrimer registro en la tabla vacuna:")
        for row in result:
            print(dict(row))
except Exception as e:
    print(f"\nError al realizar la consulta: {str(e)}")
