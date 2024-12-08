import os
from app import create_app

def create_database():
    db_path = os.path.join(os.path.dirname(__file__), 'instance')
    if not os.path.exists(db_path):
        os.makedirs(db_path)  # Создаст папку, если она не существует

    app = create_app()
    with app.app_context():
        from app.db import init_db
        init_db(app)

if __name__ == "__main__":
    create_database()
