from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

login_manager = LoginManager()

# Настройка перенаправления на страницу логина при неаутентифицированном доступе
login_manager.login_view = 'login'
