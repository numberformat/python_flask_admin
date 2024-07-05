from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectMultipleField
from flask_admin.form.widgets import Select2Widget
from flask_sqlalchemy import SQLAlchemy
from model import Role, User
from shared import db

class PostView(ModelView):
    can_delete = False
    form_columns = ["title", "body", "user"]
    column_list = ["title", "body", "user"]

class UserView(ModelView):
    form_columns = ["name", "posts", "roles"]
    page_size = 2
    #can_delete = False
    #can_create = False
    #can_edit = False

    # If your model has too much data to display in the list view, you can add a read-only details view by setting:
    can_view_details = True

    #column_exclude_list = ['password', ]
    #column_searchable_list = ['name', 'email']
    #column_filters = ['country']

    # For a faster editing experience, enable inline editing in the list view:
    column_editable_list = ['name']

    # have the add & edit forms display inside a modal window on the list page, instead of the dedicated create & edit pages:
    create_modal = True
    edit_modal = True

    # You can restrict the possible values for a text-field by specifying a list of select choices:
    form_choices = {
        'title': [
            ('MR', 'Mr'),
            ('MRS', 'Mrs'),
            ('MS', 'Ms'),
            ('DR', 'Dr'),
            ('PROF', 'Prof.')
        ]
    }

    # To remove fields from the create and edit forms:
    form_excluded_columns = ['last_name', 'email']

    # To specify arguments to the WTForms widgets used to render those fields:
    #form_widget_args = {
    #    'description': {
    #        'rows': 10,
    #        'style': 'color: black'
    #    }
    #}

    # To enable csv export of the model view:
    can_export = True

    # This will create a top-level menu item named ‘Team’, and a drop-down containing links to the three views.
    #admin.add_view(UserView(User, db.session, category="Team"))
    #admin.add_view(ModelView(Role, db.session, category="Team"))
    #admin.add_view(ModelView(Permission, db.session, category="Team"))

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
