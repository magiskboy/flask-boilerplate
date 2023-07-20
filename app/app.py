from flask import Flask
from app.extensions.database import configure_database
from app.extensions.login_manager import configure_login_manager
from app.extensions.logging import get_logger
from app.extensions.super_admin import configure_super_admin
from app.config import get_config
from app.modules import auth


logger = get_logger(__name__)


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)

    # load configuration
    config = get_config(config_name)
    app.config.from_object(config)
    logger.info(f"Current configuration:\n{config.to_str()}")

    # configure extension modules
    configure_database(app)
    configure_login_manager(app)
    configure_super_admin(app)

    # load modules
    auth.init_app(app)

    return app
