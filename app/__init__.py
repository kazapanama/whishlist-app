import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='../static')
    
    # Use environment variable for production or default for development
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///wishlist.db')
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # Configure upload folder
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'uploads')
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Ensure the upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    db.init_app(app)
    
    from app.routes import main_bp, admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    with app.app_context():
        db.create_all()
    
    return app