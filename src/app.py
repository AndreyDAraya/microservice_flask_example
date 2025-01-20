import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flasgger import Swagger

from src.config import config
from src.infrastructure.database.models import db
from src.interfaces.rest.controllers import api

def create_app(config_name=None):
    """Fábrica de aplicación Flask"""
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Configurar JSON encoder para manejar caracteres UTF-8
    app.json.ensure_ascii = False

    # Inicializar extensiones
    db.init_app(app)
    Migrate(app, db)
    jwt = JWTManager(app)
    CORS(app)

    # Configurar JWT para extraer el token del header
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    
    Swagger(app)

    # Registrar blueprints
    app.register_blueprint(api, url_prefix='/api/v1')

    @app.route('/health')
    def health_check():
        """Endpoint de verificación de salud"""
        return {'status': 'healthy'}, 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000)