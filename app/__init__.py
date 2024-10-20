from flask import Flask
from app.extensions import db, migrate
from app.config import Config
from app.routes import init_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Инициализация маршрутов
    init_routes(app)
    
    return app
