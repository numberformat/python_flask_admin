from flask import Flask, render_template
from flask_admin import Admin, AdminIndexView, expose
from flask import Blueprint

from model import User, Post, Group
from view import UserView, PostView, GroupView
from shared import db, generate_schema
from adminapi_blueprint import adminapi_blueprint
import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

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

    app.register_blueprint(adminapi_blueprint, url_prefix='/adminapi')
    # now resources from the adminapi route can be accessed at /adminapi
    # you will need to create a new ProxyPass and ProxyPassReverse rules in your apache configuration
    #     ProxyPass /adminapi http://localhost:5000/adminapi
    #     ProxyPassReverse /adminapi http://localhost:5000/adminapi

    with app.app_context():
        generate_schema(db=db)
        print("Schema generated successfully.")

    return app