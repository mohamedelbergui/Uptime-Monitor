from flask import Flask
from app.config import DevelopmentConfig
from app.extensions import db, migrate, login_manager
import app.models

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initializing extensions
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    login_manager.login_view='auth.login'

    # Recording of Blueprints
    from app.routes import main_bp
    from app.routes import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app