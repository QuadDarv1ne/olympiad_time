import os
import shutil
from app import create_app
import logging
from logging.handlers import RotatingFileHandler

# Определяем BASE_DIR как корневую директорию проекта
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
TEMP_DIR = os.path.join(BASE_DIR, 'temp')

# Определяем конфигурацию на основе переменной окружения
config_name = os.getenv('FLASK_CONFIG', 'development')

# Создаем приложение с помощью функции create_app
app = create_app(config_name)

# Функция для настройки логирования
def setup_logging():
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)  # Создаем директорию для логов, если она не существует
    file_handler = RotatingFileHandler(os.path.join(LOG_DIR, 'app.log'), maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')

# Функция для удаления временных файлов
def remove_temp_files(directory):
    if os.path.exists(directory):
        try:
            shutil.rmtree(directory)
            print(f"Удалена временная директория: {directory}")
        except Exception as e:
            print(f"Не удалось удалить временные файлы из {directory}: {e}")
    else:
        print(f"Временная директория {directory} не существует.")

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

# Удаляем __pycache__, временные файлы и старые логи перед запуском приложения
remove_pycache(BASE_DIR)
remove_temp_files(TEMP_DIR)

# Удаление старых логов (кроме последних 10 файлов)
def remove_old_logs(log_directory, keep_count=10):
    if os.path.exists(log_directory):
        log_files = sorted(
            [os.path.join(log_directory, f) for f in os.listdir(log_directory) if os.path.isfile(os.path.join(log_directory, f))],
            key=os.path.getmtime
        )
        if len(log_files) > keep_count:
            for log_file in log_files[:-keep_count]:
                try:
                    os.remove(log_file)
                    print(f"Удален старый лог: {log_file}")
                except Exception as e:
                    print(f"Не удалось удалить лог {log_file}: {e}")

remove_old_logs(LOG_DIR)

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
