from app.app import create_app
from app.config import get_env


env = get_env("ENV", "production")
app = create_app(env)
