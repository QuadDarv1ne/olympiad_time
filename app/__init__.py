from flask import Flask
from flask_login import LoginManager
from app.extensions import db, migrate, login_manager
from app.routes import init_routes
from config import Config
import logging
from logging.handlers import RotatingFileHandler
from flask_migrate import Migrate

# Инициализация LoginManager
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)

    # Инициализация Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Инициализация маршрутов
    init_routes(app)

    # Настройка логирования
    setup_logging(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

def setup_logging(app):
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
