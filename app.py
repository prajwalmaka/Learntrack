import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///learntrack.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# File upload configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

with app.app_context():
    # Import models to ensure tables are created
    import models
    db.create_all()
    # Ensure the real admin user exists
    from models import create_default_admin
    create_default_admin()
    
    # Create default admin user if none exists
    from models import User
    from werkzeug.security import generate_password_hash
    
    if not User.query.filter_by(email='admin@learntrack.com').first():
        admin_user = User(
            email='admin@learntrack.com',
            name='Admin User',
            role='teacher',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Default admin user created: admin@learntrack.com / admin123")

# Import and register blueprints
from routes import auth_bp, teacher_bp, student_bp, main_bp, admin_bp
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(teacher_bp, url_prefix='/teacher')
app.register_blueprint(student_bp, url_prefix='/student')
app.register_blueprint(main_bp)
app.register_blueprint(admin_bp)

# --- Notification context processor and mark-as-read route ---
from flask import current_app, jsonify, g
from flask_login import current_user, login_required
from models import Notification

@app.context_processor
def inject_notifications():
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).limit(10).all()
        unread_notifications = [n for n in notifications if not n.is_read]
        return dict(
            notifications=notifications,
            unread_notifications=unread_notifications
        )
    return dict(notifications=[], unread_notifications=[])

@app.route('/notification/read/<int:notif_id>', methods=['POST'])
@login_required
def mark_notification_read(notif_id):
    notif = Notification.query.filter_by(id=notif_id, user_id=current_user.id).first_or_404()
    notif.is_read = True
    db.session.commit()
    return jsonify({'success': True})
