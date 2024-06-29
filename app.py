from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectMultipleField
from flask_admin.form.widgets import Select2Widget

db = SQLAlchemy()
admin = Admin(name='MyApp', template_mode='bootstrap3')

# Define the association table for the many-to-many relationship
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    posts = db.relationship("Post", back_populates="user")
    roles = db.relationship('Role', secondary=roles_users, back_populates='users', lazy='dynamic')

    def __str__(self):
        return self.name

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    user_id = db.Column(db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="posts")

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', secondary=roles_users, back_populates='roles')
    
    def __str__(self):
        return self.name
    
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

admin.add_view(UserView(User, db.session))
admin.add_view(PostView(Post, db.session))
admin.add_view(RoleView(Role, db.session))

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SECRET_KEY"] = "mysecret"
    db.init_app(app)
    admin.init_app(app)
    @app.route("/")
    def index():
        return render_template("index.html")
    
    return app