from flask import Flask, jsonify, request
from models import db, User,Question,Like,Answer
from flask_cors import CORS



app = Flask(__name__)
CORS(app)  # Apply CORS settings to the Flask app

@app.after_request
def add_cors_headers(response):
    # Add CORS headers to the response
    response.headers.add('Access-Control-Allow-Origin', '*') # Allow requests from this origin
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization') # Allow specific headers
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE') # Allow specific HTTP methods
    return response
# Configure the database connection settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oasis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# user  routes

@app.route('/users', methods=["GET"])
def get_users():
    users = User.query.all()
    user_list = [user.to_dict() for user in users]
    return jsonify(users=user_list)

@app.route('/user/<int:user_id>', methods=["GET"])
def user_profile(user_id):
    profile = User.query.get(user_id)
    if profile:
        return jsonify(profile.to_dict())
    else:
        return jsonify({'error': 'Profile not found.'}), 404

@app.route('/users/register', methods=["POST"])
def register_user():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    profile = request.json['profile']
    new_user = User(name=name, email=email, password=password,profile=profile)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully.', 'user': new_user.to_dict()}), 201

@app.route('/users/login', methods=["POST"])
def login():
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        return jsonify({'message': 'Login successful.', 'user': user.to_dict()})
    else:
        return jsonify({'error': 'Invalid email or password.'}), 401

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'user deleted successfully.'})
    else:
        return jsonify({'error': 'user not found.'}), 404

@app.route('/users/<int:id>', methods=['PUT'])
def update_user_info():
    user = Question.query.get(id)
    if user:
       user.name = request.json['title']
       user.profile = request.json['content']
       user.email = request.json['user_id']
       db.session.commit()
       return jsonify({'message': 'user updated successfully.', 'user': user.to_dict()})
    else:
        return jsonify({'error': 'user not found.'}), 404

#Question Routes
@app.route('/questions',methods=['GET'])
def get_questions():
    questions = Question.query.all()
    question_list = [quest.to_dict() for quest in questions]
    return jsonify(quest = question_list)


@app.route('/questions/<int:id>',methods=['GET'])
def get_question_by_id(quest_id):
    question = Question.query.get(quest_id)
    if question:
        return jsonify(question.to_dict())
    else:
        return jsonify({'error': 'question not found.'}), 404

@app.route('/question/create',methods=['POST'])
def create_question():
    title = request.json['title']
    content = request.json['content']
    user_id = request.json['user_id']
    new_question = Question(title=title,content=content,user_id=user_id)
    db.session.add(new_question)
    db.session.commit()
    return jsonify({'message': 'Qusetion added successfully.', 'user': new_question.to_dict()}), 201


@app.route('/question/<int:id>',methods=["PUT"])
def update_question(id):
    quest = Question.query.get(id)
    if quest:
        quest.title = request.json['title']
        quest.content = request.json['content']
        quest.user_id = request.json['user_id']
        db.session.commit()
        return jsonify({'message': 'quest updated successfully.', 'quest': quest.to_dict()})
    else:
        return jsonify({'error': 'question not found.'}), 404



@app.route('/question/<int:id>',methods=["DELETE"])
def delete_question():
    question = Question.query.get(id)
    if question:
        db.session.delete(question)
        db.session.commit()
        return jsonify({'message': 'question deleted successfully.'})
    else:
        return jsonify({'error': 'question not found.'}), 404

# like qestion rotes
@app.route('/question/<int:question_id>/like', methods=['POST'])
def create_like(question_id):
    # Get the question by ID
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'question not found'}), 404

    # Get the data from the request
    user_id = request.json.get('user_id')

    # Check if user has already liked the question
    existing_like = Like.query.filter_by(user_id=user_id, question_id=question.id).first()
    if existing_like:
        return jsonify({'message': 'You have already liked this question'}), 400

    # Create a new like
    like = Like(user_id=user_id, question_id=question.id)
    db.session.add(like)
    db.session.commit()

    return jsonify({'message': 'Like created successfully', 'like_id': like.id}), 201


# Route to get all likes for a question
@app.route('/question/<int:question_id>/likes', methods=['GET'])
def get_likes(question_id):
    # Get the question by ID
    question = question.query.get(question_id)
    if not question:
        return jsonify({'error': 'question not found'}), 404

    # Get all likes for the question
    likes = Like.query.filter_by(question_id=question.id).all()

    # Convert likes to a list of dictionaries
    likes_dict = [like.to_dict() for like in likes]

    return jsonify({'likes': likes_dict}), 200




# Route to create a new Answer for a Question
@app.route('/question/<int:question_id>/answer', methods=['POST'])
def create_answer(question_id):
    # Get the question by ID
    quest = Question.query.get(question_id)
    if not quest:
        return jsonify({'error': 'question not found'}), 404

    # Get the data from the request
    content = request.json.get('content')
    user_id = request.json.get('user_id')
    question = request.json.get('question')
    topic = request.json.get('topic')

    # Check if content is provided
    if not content:
        return jsonify({'error': ' content is required'}), 400

    # Check if user_id is provided
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    # Create a new comment
    answer = Answer(content=content, user_id=user_id, question=question,topic=topic)
    db.session.add(answer)
    db.session.commit()

    return jsonify({'message': 'Answer added successfully', 'comment_id': question}), 201


# Route to get all answers for a question
@app.route('/question/<int:quest_id>/answers', methods=['GET'])
def get_answers(quest_id):
    # Get the question by ID
    question = Question.query.get(quest_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    # Get all answers for the question
    answer = Answer.query.filter_by(quest_id=quest_id).all()

    # Convert answers to a list of dictionaries
    answers_dict = [answers.to_dict() for answers in answer]

    return jsonify({'answers': answers_dict }), 200


if __name__ == '__main__':
    with app.app_context():  
        db.create_all()  
    app.run(debug=True)

