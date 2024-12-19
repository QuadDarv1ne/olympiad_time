import os
from flask import Flask
from flask_login import LoginManager
from app.routes import init_routes
from config import config
import logging
from logging.handlers import RotatingFileHandler
from app.db.database import db, migrate
from app.db import init_db

login_manager = LoginManager()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')  # Получаем конфигурацию из переменных окружения
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Вызываем init_app, если он присутствует в конфигурации
    if hasattr(config[config_name], 'init_app'):
        config[config_name].init_app(app)

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)

    # Настройка Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Инициализация маршрутов
    init_routes(app)

    # Создание таблиц, если их нет (для разработки)
    with app.app_context():
        if not os.path.exists(app.config['DB_DIR']):
            os.makedirs(app.config['DB_DIR'])
        db.create_all()

    # Настройка логирования
    setup_logging(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.db.models import Account
    user = Account.query.get(int(user_id))
    if user is None:
        # Логируем ошибку, если пользователь не найден
        logging.warning(f"User with ID {user_id} not found.")
    return user

def setup_logging(app):
    """Настройка логирования приложения."""
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    handler = RotatingFileHandler(os.path.join(log_dir, 'app.log'), maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.info("Logging is set up.")
