from flask import Flask
from .config import Config
from flask_wtf import CSRFProtect

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    csrf.init_app(app)

    # Register blueprints
    from .blueprints.main import main
    app.register_blueprint(main)

    return app
