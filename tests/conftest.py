from unittest import mock
import pytest
import sqlalchemy as sa
from werkzeug.local import LocalProxy
from app.app import create_app
from app.extensions.database import db
from .abic_faker import ABICFaker


@pytest.fixture(scope="module")
def client(faker):
    with mock.patch("flask_login.utils.current_user") as mock_request_loader:
        _app = create_app("testing")

        with _app.app_context():
            # Issue with sqlite here: https://stackoverflow.com/questions/2614984/sqlite-sqlalchemy-how-to-enforce-foreign-keys?rq=1
            sa.event.listen(
                db.engine,
                "connect",
                lambda con, record: con.execute('pragma foreign_keys=ON'))

            db.create_all()

            mock_request_loader.return_value = LocalProxy(lambda: faker.user())
            with _app.test_client() as client:
                yield client


@pytest.fixture(scope="module")
def faker():
    return ABICFaker()
