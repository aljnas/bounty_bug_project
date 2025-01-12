from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bounty_bug.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar la base de datos
    db.init_app(app)

    # Importar y registrar Blueprints
    from app.routes.main import bp as main_bp
    from app.routes.analyzer import analyzer_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(analyzer_bp, url_prefix="/api")

    return app
