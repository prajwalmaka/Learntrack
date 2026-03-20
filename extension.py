from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase

db = SQLAlchemy()
login_manager = LoginManager()