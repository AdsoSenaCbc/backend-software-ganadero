from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate

# Inicialización de extensiones
db = SQLAlchemy()
jwt = JWTManager()
login_manager = LoginManager()
login_manager.login_message = "Por favor inicia sesión para acceder a esta página."
migrate = Migrate()

def create_app():
    import os
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__,
                template_folder=os.path.join(base_dir, '..', 'templates'),
                static_folder=os.path.join(base_dir, '..', 'static'))

    # Configuración
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/sistema_ganadero_database'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'tu-clave-secreta-aqui'  # Cambia por una clave segura y única
    app.config['SECRET_KEY'] = 'otra-clave-secreta'  # Cambia por una clave segura y única
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False  # Cambia a True en producción con HTTPS
    app.config['JWT_ACCESS_CSRF_PROTECT'] = False  # Activa en producción

    # Inicialización de extensiones
    db.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    migrate.init_app(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.usuario import Usuario
        return Usuario.query.get(int(user_id))

    with app.app_context():
        import importlib
        blueprints = {
            'auth': ('auth', '/auth'),
            'dashboard': ('main', '/'),
            'animal': ('animal', '/api/animals'),
            'caracteristicas_nutricionales': ('caracteristicas_nutricionales', '/api/caracteristicas-nutricionales'),
            'condiciones_especiales': ('condiciones_especiales', '/api/condiciones-especiales'),
            'consulta_bromatologica': ('consulta_bromatologica', '/api/consultas-bromatologicas'),
            'materia_prima': ('materia_prima', '/api/materias-primas'),
            'consulta_ingredientes': ('consulta_ingredientes', '/api/consultas-ingredientes'),
            'departamento': ('departamento', '/api/departamentos'),
            'detalle_racion': ('detalle_racion', '/api/detalles-racion'),
            'detalle_racion_nutricional': ('detalle_racion_nutricional', '/api/detalles-racion-nutricional'),
            'especie': ('especie', '/api/especies'),
            'estado_animal': ('estado_animal', '/api/estados-animal'),
            'etapas_productivas': ('etapas_productivas', '/api/etapas-productivas'),
            'evento_animal': ('evento_animal', '/api/eventos-animal'),
            'hacienda': ('hacienda', '/api/haciendas'),
            'historial_animal': ('historial_animal', '/api/historiales-animal'),
            'historial_hacienda': ('historial_hacienda', '/api/historiales-hacienda'),
            'ingrediente': ('ingrediente', '/api/ingredientes'),
            'ingrediente_materia_prima': ('ingrediente_materia_prima', '/api/ingredientes-materia-prima'),
            'lote_vacuna': ('lote_vacuna', '/api/lotes-vacuna'),
            'materia_prima': ('materia_prima', '/api/materias-prima'),
            'municipio': ('municipio', '/api/municipios'),
            'nacimiento': ('nacimiento', '/api/nacimientos'),
            'nutrientes': ('nutrientes', '/api/nutrientes'),
            'racion': ('racion', '/api/raciones'),
            'raza': ('raza', '/api/razas'),
            'requerimientos_condiciones': ('requerimientos_condiciones', '/api/requerimientos-condiciones'),
            'requerimientos_nrc': ('requerimientos_nrc', '/api/requerimientos-nrc'),
            'requerimientos_nutricionales': ('requerimientos_nutricionales', '/api/requerimientos-nutricionales'),
            'rol_usuario': ('rol_usuario', '/api/roles-usuario'),
            'sexo': ('sexo', '/api/sexos'),
            'tipo_evento': ('tipo_evento', '/api/tipos-evento'),
            'user': ('user', '/api/users'),
            'vacuna': ('vacuna', '/api/vacunas'),
            'vacunacion_animal': ('vacunacion_animal', '/api/vacunaciones-animal')
        }

        for bp_name, (module_name, url_prefix) in blueprints.items():
            module = importlib.import_module(f'app.routes.{module_name}')
            bp = getattr(module, f'{bp_name}_bp')
            app.register_blueprint(bp, url_prefix=url_prefix)
            # Garantizar que cada blueprint exponga un endpoint 'index' para su ruta raíz
          #  if f'{bp_name}.index' not in app.view_functions:
           #     root_rule = url_prefix.rstrip('/') + '/'
                # Buscar un view_func existente para la ruta raíz
                #existing_endpoint = None
                #for rule in app.url_map.iter_rules():
                #    if rule.rule == root_rule and rule.endpoint.startswith(f'{bp_name}.') and 'GET' in rule.methods:
                #        existing_endpoint = rule.endpoint
                #        break
                #if existing_endpoint:
                 #   app.add_url_rule(root_rule, endpoint=f'{bp_name}.index', view_func=app.view_functions[existing_endpoint], methods=['GET'])

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

