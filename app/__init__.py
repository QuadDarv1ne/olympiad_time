from flask import Flask
from flask_login import LoginManager
from app.extensions import db, migrate
from config import Config
from app.routes import init_routes

# Создание экземпляра LoginManager
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Инициализация Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # Укажите имя маршрута для страницы входа

    # Инициализация маршрутов
    init_routes(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    # Замените на вашу логику для загрузки пользователя из базы данных
    from app.models import User  # Импортируйте вашу модель User
    return User.query.get(int(user_id))
