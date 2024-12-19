import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Основные настройки приложения."""

    # Секретный ключ для защиты сессий и шифрования
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Настройки базы данных
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_DIR = os.path.join(BASE_DIR, 'instance')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Настройки почтового сервера
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', '1', 't']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    @classmethod
    def init_app(cls, app):
        """Инициализация конфигурации приложения."""
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL') or f'sqlite:///{os.path.join(Config.DB_DIR, "dev_olympiad_time.db")}'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL') or f'sqlite:///{os.path.join(Config.DB_DIR, "test_olympiad_time.db")}'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URL') or f'sqlite:///{os.path.join(Config.DB_DIR, "prod_olympiad_time.db")}'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # Настройка логирования
        import logging
        from logging.handlers import SMTPHandler, RotatingFileHandler

        if cls.MAIL_SERVER:
            auth = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            secure = () if cls.MAIL_USE_TLS else None
            mail_handler = SMTPHandler(
                mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
                fromaddr=cls.MAIL_USERNAME,
                toaddrs=[cls.MAIL_USERNAME],
                subject='Application Error',
                credentials=auth,
                secure=secure,
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.makedirs('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Application startup')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
