from datetime import datetime
import jwt
from flask import Flask, Request, current_app
from flask_login import LoginManager
from app.extensions import logging
from app.models import User


logger = logging.get_logger(__name__)

login_manager = LoginManager()


def jwt_encode(payload: dict) -> str:
    return jwt.encode(
        payload={
            **payload,
            "exp": datetime.utcnow() + current_app.config.get("JWT_EXPIRED_TIME"),
        },
        key=current_app.config.get("JWT_KEY"),
        algorithm=current_app.config.get("JWT_ALGORITHMS")[0],
    )


def jwt_decode(token: str) -> dict:
    try:
        return jwt.decode(
            jwt=token,
            key=current_app.config.get("JWT_KEY"),
            verify=True,
            algorithms=current_app.config.get("JWT_ALGORITHMS"),
            options={
                "exp": True, 
            }
        )
    except jwt.DecodeError:
        return None


@login_manager.request_loader
def request_loader(request: Request) -> User | None:
    signature = request.headers.get("Authorization")
    if not signature:
        return None

    if not signature.startswith("Bearer "):
        return None

    token = signature.removeprefix("Bearer ")
    payload = jwt_decode(token)

    if payload:
        username = payload.get("username")
        
        if not username:
            return None

        return User.get_by_username(username)

    else:
        logger.debug("Signature decode failed")
        return None


def configure_login_manager(app: Flask):
    logger.info("Configure login_manager...")

    login_manager.init_app(app)
