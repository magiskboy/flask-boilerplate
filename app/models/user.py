from typing import Union
from enum import Enum
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions.database import db
from app.extensions.super_admin import register_view


class UserRole(str, Enum):
    collaborator = "collaborator"
    agent        = "agent"
    admin        = "admin"


class User(UserMixin, db.Model):
    username = db.Column(db.String(20), unique=True, nullable=False)
    hash_password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)

    @property
    def password(self):
        raise AttributeError("password is a secret")

    @password.setter
    def password(self, raw_password: str):
        self.hash_password = generate_password_hash(raw_password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.hash_password, password)

    def __str__(self) -> str:
        return f"<User {self.username}>"

    def get_id(self) -> int:
        return self.id_

    @classmethod
    def get_by_username(cls, username: str) -> Union["User", None]:
        return db.session.query(cls).filter(cls.username==username).first()


register_view(User)
