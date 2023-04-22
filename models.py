from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from datetime import datetime  # Import datetime for handling timestamps

from datetime import datetime
# Create an instance of SQLAlchemy
db = SQLAlchemy()


#user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile = db.Column(db.String(255))
    bio = db.Column(db.String(400))
    isAdmin = db.Column(db.Boolean,default = False)
    isModerator = db.Column(db.Boolean,default = False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name, email, password, profile,isAdmin,isModerator):
        self.name = name
        self.email = email
        self.password = password
        self.profile = profile
        self.isAdmin = isAdmin
        self.isModerator = isModerator

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'profile': self.profile,
            'isAdmin':self.isAdmin,
            'isModerator':self.isModerator,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }



# Class definition for Question model

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('questions', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    answers = db.relationship('Answer', backref='question', lazy=True) # Added Answers relationship
    

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
    topic = db.Column(db.String(300),nullable=False)
    user = db.relationship('User', backref=db.backref('answers', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, content, user_id, question,topic):
        self.content = content
        self.user_id = user_id
        self.question = question
        self.topic = topic
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
            'topic':self.topic,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


# Class definition for Like model

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('likes', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id
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
            'post_id': self.post_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

#definition for the upvote model
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

#definition for the downvote model
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
    
    #community model
class Community(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    logo = db.Column(db.String(255))
    name = db.Column(db.String(200),nullable = False)
    description = db.Column(db.Text, nullable = False)
    members = db.relationship('Member', backref=db.backref('community',lazy=True)) 
    posts = db.relationship('Post',backref=db.backref('community',lazy=True))
    user = db.relationship('User', backref=db.backref('answers', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self,user_id,name,description,logo):
        self.user_id = user_id
        self.name = name
        self.description = description
        self.logo = logo
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return{
            'id': self.id,
            'user_id': self.user_id,
            'name:':self.name,
            'description':self.description,
            'logo':self.logo,
            'posts': [post.to_dict() for post in self.posts],
            'members':[member.to_dict() for member in self.members],
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
# model for community members

class Member(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'), nullable=False)
    username = db.Column(db.String(200),nullable=False) 
    profile = db.Column(db.String(200))
    bio = db.Column(db.Text,nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self,community_id,username,profile,bio):
        self.username = username
        self.profile = profile
        self.bio = bio
        self.community_id = community_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return{
            'id':self.id,
            'community_id':self.community_id,
            'username':self.username,
            'profile':self.profile,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

# this is the model for adding a post to a community
class Post(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text,nullable = False)
    commnunity_id = db.Column(db.Integer, db.ForeignKey('community.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True) 
    likes = db.relationship('Like', backref='post', lazy=True) # Added likes relationship
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self,user_id,content,community_id):
        self.user_id = user_id
        self.content = content
        self.community_id = community_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return{
            'id':self.id,
            'user_id':self.user_id,
            'community_id':self.community_id,
            'content':self.content,
            'comments':[comment.to_dict() for comment in self.comments],
            'likes':[like.to_dict() for like in self.likes],
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
#model for adding comment to a post in a community
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, content, user_id, post_id):
        self.content = content
        self.user_id = user_id
        self.post_id = post_id
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
            'post_id': self.post_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }