import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Основные настройки приложения."""
    
    # Секретный ключ для защиты сессий и шифрования
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_secret_key'

    # Настройки базы данных
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Получаем абсолютный путь к директории проекта
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "instance", "olympiad_time.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Отключение отслеживания изменений для уменьшения использования памяти

    # Настройки почтового сервера
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # Почта для отправки сообщений
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # Пароль для почтового аккаунта

    @classmethod
    def init_app(cls, app):
        """Инициализация конфигурации приложения."""
        pass  # Место для расширяемой логики инициализации приложения
