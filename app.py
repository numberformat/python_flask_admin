from flask import Flask, render_template
from flask_admin import Admin, AdminIndexView, expose
from flask import Blueprint
import os.path as op

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

    # adding static resources
    # since /admin is already used by Flask-Admin, we need to use a different route to serve the static files
    # the following code adds an /adminstatic route to serve the static files from the admin blueprint
    # use "{{ url_for('adminstatic.static', filename='schema.png') }}" to access the schema.png file
    path = op.join(op.dirname(__file__), 'static')

    admin_blueprint = Blueprint('adminstatic', __name__,
                            static_folder=path,
                            static_url_path='/')

    app.register_blueprint(admin_blueprint, url_prefix='/adminstatic')
    # now files from the static folder can be accessed at /adminstatic
    # you will need to create a new ProxyPass and ProxyPassReverse rules in your apache configuration
    #     ProxyPass /adminstatic http://localhost:5000/adminstatic
    #     ProxyPassReverse /adminstatic http://localhost:5000/adminstatic

    return app