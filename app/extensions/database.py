import re
from pydantic import BaseModel as PydanticBaseModel, ConfigDict
from flask import Flask
from flask_sqlalchemy import SQLAlchemy, model
import sqlalchemy as sa
from flask_migrate import Migrate
from app.extensions import logging


logger = logging.get_logger(__name__)


class BaseSchema(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_: int


class BaseModel(model.Model):
    @sa.orm.declared_attr
    def __tablename__(cls):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()

    id_ = sa.Column("id", sa.Integer(), primary_key=True)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.sql.func.now())
    updated_at = sa.Column(sa.DateTime(timezone=True), onupdate=sa.sql.func.now())

    def __str__(self):
        return f"<{self.__class__.__name__()} {self.id_}>"


db = SQLAlchemy(
    add_models_to_shell=True,
    model_class=BaseModel,
)

migrate = Migrate(db=db)


def configure_database(app: Flask):
    logger.info("Configure database...")
    db.init_app(app)
    migrate.init_app(app)
