# run.py
import os
from app import create_app
import logging
from logging.handlers import RotatingFileHandler

# Определяем конфигурацию на основе переменной окружения
config_name = os.getenv('FLASK_CONFIG') or 'default'

# Создаем приложение с помощью функции create_app
app = create_app(config_name)

# Функция для настройки логирования
def setup_logging():
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')

# Запуск приложения
if __name__ == "__main__":
    # Настройка логирования
    setup_logging()

    try:
        # Запуск сервера на 127.0.0.1 с портом 8080
        app.run(debug=True, host="127.0.0.1", port=8080)
    except Exception as e:
        app.logger.error(f"Failed to start the application: {e}")
