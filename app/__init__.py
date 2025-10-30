import os

from flask import Flask

from .config import Config
from . import data


def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(__name__, instance_relative_config=True, static_folder="static", template_folder="templates")
    app.config.from_object(config_class)

    os.makedirs(app.config["INSTANCE_DIR"], exist_ok=True)

    data.init_app(app)

    from .blueprints.main import main as main_bp
    from .blueprints.shop import shop as shop_bp
    from .blueprints.custom import custom as custom_bp
    from .blueprints.media import media as media_bp
    from .blueprints.checkout import checkout as checkout_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(shop_bp, url_prefix="/shop")
    app.register_blueprint(custom_bp, url_prefix="/custom")
    app.register_blueprint(media_bp, url_prefix="/videos")
    app.register_blueprint(checkout_bp)

    return app
