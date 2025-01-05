import os
import shutil
from app import create_app
import logging
from logging.handlers import RotatingFileHandler

# Определяем BASE_DIR как корневую директорию проекта
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Определяем конфигурацию на основе переменной окружения
config_name = os.getenv('FLASK_CONFIG', 'development')

# Создаем приложение с помощью функции create_app
app = create_app(config_name)

# Функция для настройки логирования
def setup_logging():
    if not os.path.exists('logs'):
        os.mkdir('logs')  # Создаем директорию для логов, если она не существует
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')

# Функция для удаления __pycache__ в директории проекта
def remove_pycache(directory):
    for root, dirs, files in os.walk(directory):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(pycache_path)
                print(f"Удалена папка {pycache_path}")
            except Exception as e:
                print(f"Не удалось удалить папку {pycache_path}: {e}")

# Удаляем __pycache__ в проекте перед запуском приложения
remove_pycache(BASE_DIR)

# Запуск приложения
if __name__ == "__main__":
    # Настройка логирования
    setup_logging()

    try:
        # Запуск сервера на 127.0.0.1 с портом 8080
        app.run(debug=True, host="127.0.0.1", port=8080)
    except Exception as e:
        app.logger.error(f"Failed to start the application: {e}")
        # Выводим ошибку в консоль
        print(f"Failed to start the application: {e}")
