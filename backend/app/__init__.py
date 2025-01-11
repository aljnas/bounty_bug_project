from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bounty_bug.db'  # Configuración de la base de datos
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Importa y registra los blueprints si los tienes
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
