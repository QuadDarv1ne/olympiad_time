# app/asgi.py
from app import create_app

app = create_app()

# В Flask 2.x вы можете использовать синхронные и асинхронные обработчики.
# uvicorn будет запускать приложение как ASGI сервер
