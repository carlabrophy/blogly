import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


default_img = "https://as2.ftcdn.net/v2/jpg/01/36/70/67/1000_F_136706734_KWhNBhLvY5XTlZVocpxFQK1FfKNOYbMj.jpg"


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15))
    image_url = db.Column(db.Text, default=default_img)
    posts = db.relationship('Post', backref='user', cascade="all, delete")
    


    def __repr__(self):
        """Show ouput"""
        return f"<{self.id},  {self.first_name}, {self.last_name}>"


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True )
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    posts_tags = db.relationship('PostTag', cascade="all, delete" ,backref='post')

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")



class PostTag(db.Model):
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    
    


class Tag(db.Model):
    __tablename__= 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        cascade="all, delete",
        backref="tags",
    )