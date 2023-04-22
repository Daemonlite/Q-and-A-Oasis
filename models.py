from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from datetime import datetime  # Import datetime for handling timestamps

from datetime import datetime
# Create an instance of SQLAlchemy
db = SQLAlchemy()



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name, email, password, profile):
        self.name = name
        self.email = email
        self.password = password
        self.profile = profile

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'profile': self.profile,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }



# Class definition for Post model

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('questions', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    answers = db.relationship('Answer', backref='question', lazy=True) # Added Answers relationship
    likes = db.relationship('Like', backref='question', lazy=True) # Added likes relationship

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.created_at = datetime.utcnow()  # Set initial value for created_at
        self.updated_at = datetime.utcnow()  # Set initial value for updated_at

    def to_dict(self):
 
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'answers': [answer.to_dict() for answer in self.answers], # Added answers to dictionary
            'likes': [like.to_dict() for like in self.likes] # Added likes to dictionary
        }

# Class definition for answer model

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('answers', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, content, user_id, question):
        self.content = content
        self.user_id = user_id
        self.question = question
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """
        Convert Comment model instance to a dictionary.

        Returns:
        dict: A dictionary representing the Comment model instance.
        """
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'question': self.question,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


# Class definition for Like model

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('likes', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, user_id, question_id):
        self.user_id = user_id
        self.question_id = question_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """
        Convert Like model instance to a dictionary.

        Returns:
        dict: A dictionary representing the Like model instance.
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class UpVote(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('votes', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self,user_id,question_id,user):
        self.user_id = user_id
        self.question_id = question_id
        self.user = user
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return{
             'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class DownVote(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('votes', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self,user_id,question_id,user):
        self.user_id = user_id
        self.question_id = question_id
        self.user = user
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return{
             'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }