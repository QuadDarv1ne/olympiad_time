# app/__init__.py
from flask import Flask
from flask_login import LoginManager
from app.routes import init_routes
from config import Config
import logging
from logging.handlers import RotatingFileHandler
from app.db.database import db, migrate  # Импортируем db и migrate
from app.db import init_db  # Импортируем инициализацию базы данных

# Инициализация LoginManager
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация расширений
    db.init_app(app)  # Инициализация db
    migrate.init_app(app, db)  # Инициализация миграции

    # Настройка Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Инициализация маршрутов
    init_routes(app)

    # Создание таблиц, если их нет (для разработки)
    init_db(app)  # Передаем app

    # Настройка логирования
    setup_logging(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.db.models import Account
    return Account.query.get(int(user_id))

def setup_logging(app):
    """Настройка логирования приложения."""
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.info("Logging is set up.")
