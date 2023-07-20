import random
from typing import Optional
from functools import wraps
import string
from faker import Faker
from app.models import User, UserRole
from app.extensions.database import db


def auto_commit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        commit = kwargs.pop("commit", True)

        instance = func(*args, **kwargs)

        if commit:
            db.session.add(instance)
            db.session.commit()

        return instance
    return wrapper


class ABICFaker:
    faker = Faker()

    def substring(self, string: str) -> str:
        length = random.randint(3, len(string))
        idx = random.randint(0, len(string) - length)
        return string[idx:idx+length]

    def string(self, length: int, container = string.ascii_lowercase) -> str:
        return "".join(self.faker.random_choices(container, length))

    @auto_commit
    def user(
        self,
        role: Optional[UserRole] = None,
        password: Optional[str] = None,
    ):
        u = User(
            username=self.faker.user_name(),
            role=role or self.faker.random_element(list(UserRole)),
        )
        raw_password = password or self.faker.password()
        u.password = raw_password
        
        return u

    def __getattribute__(self, name):
        try:
            attr = object.__getattribute__(self, name)
            return attr
        except AttributeError:
            return getattr(self.faker, name)
