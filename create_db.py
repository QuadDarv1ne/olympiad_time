import os
from app import create_app

def create_database(db_filename):
    db_path = os.path.join(os.path.dirname(__file__), 'instance')
    db_file_path = os.path.join(db_path, db_filename)

    # Печать путей для отладки
    print(f"Database path: {db_path}")
    print(f"Database file path: {db_file_path}")

    # Создаем директорию для базы данных, если она не существует
    if not os.path.exists(db_path):
        print(f"Directory {db_path} does not exist. Creating...")
        os.makedirs(db_path)

    # Проверяем, существует ли база данных
    if not os.path.exists(db_file_path):
        # Устанавливаем переменную окружения для DATABASE_URL
        os.environ['DATABASE_URL'] = f'sqlite:///{db_file_path}'
        print(f"Using database URI: {os.environ['DATABASE_URL']}")
        
        app = create_app('development')  # Используем только конфигурацию для разработки
        with app.app_context():
            from app.db.database import db
            try:
                db.create_all()  # Создаем все таблицы
                print(f"Database '{db_filename}' created successfully.")
            except Exception as e:
                print(f"Error creating database: {e}")
    else:
        print(f"Database '{db_filename}' already exists.")

if __name__ == "__main__":
    db_filename = 'olympiad_time.db'
    create_database(db_filename)
