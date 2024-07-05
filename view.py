from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectMultipleField
from flask_admin.form.widgets import Select2Widget
from flask_sqlalchemy import SQLAlchemy
from model import Role, User

db = SQLAlchemy()

class PostView(ModelView):
    can_delete = False
    form_columns = ["title", "body", "user"]
    column_list = ["title", "body", "user"]

class UserView(ModelView):
    form_columns = ["name", "posts", "roles"]
    form_extra_fields = {
        'roles': QuerySelectMultipleField(
            'Roles',
            query_factory=lambda: db.session.query(Role).all(),
            widget=Select2Widget(multiple=True)
        )
    }

class RoleView(ModelView):
    form_columns = ["name", "users"]
    form_extra_fields = {
        'users': QuerySelectMultipleField(
            'Users',
            query_factory=lambda: db.session.query(User).all(),
            widget=Select2Widget(multiple=True)
        )
    }
