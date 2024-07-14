from flask import Flask, render_template
from flask_admin import Admin, AdminIndexView, expose

from model import User, Post, Group
from view import UserView, PostView, GroupView
from shared import db, generate_schema

admin = Admin(name='Example Admin Application', template_mode='bootstrap4')

admin.add_view(UserView(User, db.session, 'Users'))
admin.add_view(GroupView(Group, db.session, 'Groups'))
admin.add_view(PostView(Post, db.session, 'Posts'))

class MyAdminIndexView(AdminIndexView):
    """To generate the schema when a user navigates to /admin, we can create a new route for /admin
    in our app.py file and call the generate_schema(db) function from there.
    Since we are using Flask-Admin, which automatically handles the /admin route,
    we need to extend the Flask-Admin's AdminIndexView to include the schema generation in its index method.
    """
    @expose('/')
    def index(self):
        generate_schema(db)  # Generate the schema image
        return super(MyAdminIndexView, self).index()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SECRET_KEY"] = "mysecret"
    db.init_app(app)
    admin.init_app(app, index_view=MyAdminIndexView())

    @app.route("/")
    def index():
        return render_template("index.html")

    return app