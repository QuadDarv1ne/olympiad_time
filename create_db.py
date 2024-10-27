from app import create_app

def create_database():
    app = create_app()
    with app.app_context():
        from app.db import init_db
        init_db(app)

if __name__ == "__main__":
    create_database()
