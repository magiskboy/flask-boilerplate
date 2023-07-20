from typing import Type
from flask import Flask
from flask_admin import Admin, AdminIndexView, expose
from flask_sqlalchemy.model import Model
from flask_admin.contrib.sqla import ModelView
from flask_adminlte3 import AdminLTE3
from app.extensions.database import db


class AdminLTEModelView(ModelView):
    list_template = 'flask-admin/model/list.html'
    create_template = 'flask-admin/model/create.html'
    edit_template = 'flask-admin/model/edit.html'
    details_template = 'flask-admin/model/details.html'

    create_modal_template = 'flask-admin/model/modals/create.html'
    edit_modal_template = 'flask-admin/model/modals/edit.html'
    details_modal_template = 'flask-admin/model/modals/details.html'


class SuperAdminIndexView(AdminIndexView):
    @expose('/', methods=['GET'])
    def index(self):
        return self.render('flask-admin/base.html')


admin = Admin(
    name="Super Admin",
    template_mode="bootstrap4",
    base_template='flask-admin/base.html',
    index_view=SuperAdminIndexView(url="/super_admin", endpoint="super_admin"),
)


class BaseModelView(AdminLTEModelView):
    ...


def register_view(model: Type[Model], model_view = BaseModelView):
    admin.add_view(model_view(model, db.session))


def configure_super_admin(app: Flask):
    admin.init_app(app)
    AdminLTE3(app)
