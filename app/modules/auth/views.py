from flask import Flask, Blueprint, jsonify
from app.extensions import logging, api
from app.extensions.login_manager import jwt_encode
from app.models import User
from . import schemas


logger = logging.get_logger(__name__)


class LoginView(api.RestAPI):
    def post(self, body: schemas.LoginRequest):
        user = User.get_by_username(body.username)
        if not (user and user.verify_password(body.password)):
            return jsonify(message="username or password is wrong"), 401

        token = jwt_encode({
            "id": user.id_,
            "username": user.username,
            "role": user.role,
        })

        return jsonify(token=token)


def init_app(app: Flask):
    bp = Blueprint("auth", __name__, url_prefix="/api/auth")

    bp.add_url_rule("/login", view_func=LoginView.as_view("login"))

    app.register_blueprint(bp)
