from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()

login = LoginManager()
login.session_protection = "strong"
login.login_view = 'auth.login'
