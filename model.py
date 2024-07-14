from flask_sqlalchemy import SQLAlchemy
from shared import db

# Define the association table for the many-to-many relationship
user_group = db.Table('user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    approved = db.Column(db.Boolean, default=False)
    posts = db.relationship("Post", back_populates="user")
    groups = db.relationship('Group', secondary=user_group, back_populates='users')

    def __str__(self):
        return self.name

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    user_id = db.Column(db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="posts")

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    users = db.relationship('User', secondary=user_group, back_populates='groups')

    def __str__(self):
        return self.name