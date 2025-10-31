"""
Gym SaaS Application Factory
Multi-tenant gym management system
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Load configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    from config.config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints
    from app.routes import auth, gym, member, booking, admin, api
    app.register_blueprint(auth.bp)
    app.register_blueprint(gym.bp)
    app.register_blueprint(member.bp)
    app.register_blueprint(booking.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(api.bp)
    
    # Create database tables only if in development mode
    # In production, use migrations instead (flask db upgrade)
    if config_name == 'development':
        with app.app_context():
            try:
                db.create_all()
            except Exception as e:
                # Ignore database errors during app initialization
                # This allows the app to start even if DB is not ready
                import logging
                logging.warning(f"Failed to create database tables: {e}")
    
    return app
