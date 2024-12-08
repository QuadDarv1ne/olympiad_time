# run.py
from app import create_app

# Создаем приложение с помощью функции create_app
app = create_app()

# Запуск приложения
if __name__ == "__main__":
    # Запуск сервера на 127.0.0.1 с портом 8080
    # Для продакшн-среды рекомендуется использовать Gunicorn или uWSGI, но для разработки можно использовать встроенный сервер Flask
    app.run(debug=True, host="127.0.0.1", port=8080)
