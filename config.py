import os

class Config:
    """Основная конфигурация приложения."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')  # Пример секрета
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')  # Путь к директории базы данных
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DB_DIR, 'olympiad_time.db')  # Путь к базе данных SQLite

    @staticmethod
    def init_app(app):
        """Инициализация приложения с настройками."""
        pass

class DevelopmentConfig(Config):
    """Конфигурация для разработки."""
    DEBUG = True

class ProductionConfig(Config):
    """Конфигурация для продакшн."""
    DEBUG = False

config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
