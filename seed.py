from app import create_app, db
from app.models import RolUsuario, Usuario
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Rol admin
    admin_role = RolUsuario.query.filter_by(nombre_rol='admin').first()
    if not admin_role:
        admin_role = RolUsuario(nombre_rol='admin')
        db.session.add(admin_role)
        db.session.commit()

    # Usuario admin
    if not Usuario.query.filter_by(correo='admin@example.com').first():
        admin = Usuario(
            nombres='Admin',
            apellidos='Principal',
            documento='0001',
            correo='admin@example.com',
            telefono='0000000000',
            password=generate_password_hash('admin123'),
            id_rol=admin_role.id_rol
        )
        db.session.add(admin)
        db.session.commit()

    print("Usuario admin creado/actualizado")