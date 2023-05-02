from flask import Flask, jsonify, request
from models import db, User,Question,Like,Answer,UpVote,DownVote
from flask_cors import CORS
import bcrypt
import cloudinary
import cloudinary.uploader



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

cloudinary.config(
            cloud_name='dexc98myq',
            api_key='872169569198661',
            api_secret='AC9O0BiDuGNyfF5iipr-cBl9Gvo'
        )
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
    
    # upload profile image
    result =  cloudinary.uploader.upload(profile)
    profileImageUrl = result['secure_url']
    print(profileImageUrl)
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Create a new user with the hashed password
    new_user = User(name=name, email=email, password=hashed_password, profile=profileImageUrl)
    
    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User added successfully.', 'user': new_user.to_dict()}), 201


@app.route('/users/login', methods=["POST"])
def login():
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
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
def update_user_info(id):
    user = User.query.get(id)
    if user:
       user.name = request.json['name']
       user.profile = request.json['profile']
       user.email = request.json['email']
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
    question_id = request.json['question_id']
    topic = request.json.get('topic')

    # Check if content is provided
    if not content:
        return jsonify({'error': ' content is required'}), 400

    # Check if user_id is provided
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    # Create a new comment
    answer = Answer(content=content, user_id=user_id, question_id=question_id,topic=topic)
    db.session.add(answer)
    db.session.commit()

    return jsonify({'message': 'Answer added successfully', 'comment_id': question_id}), 201


@app.route('/answer/<int:answer_id>', methods=['DELETE'])
def delete_answer(answer_id):
    # Get the answer by ID
    answer = Answer.query.get(answer_id)
    if not answer:
        return jsonify({'error': 'answer not found'}), 404

    # Delete the answer
    db.session.delete(answer)
    db.session.commit()

    return jsonify({'message': 'Answer deleted successfully'}), 200


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


#Routes for upvotes and downvotes

@app.route('/votes/upvote/<int:vote_id>', methods=['POST'])
def vote_up(vote_id):
    # get answer by id
    answer = Answer.query.get(vote_id)

    if not answer:
        return jsonify({'error': "answer not found"})

    user_id = request.json.get('user_id')
    
     # check if user has already voted
    exist_upvote = UpVote.query.filter_by(user_id=user_id, answer_id=answer.id).first()
    exist_downvote = DownVote.query.filter_by(user_id=user_id, answer_id=answer.id).first()

    if exist_downvote:
        db.session.delete(exist_downvote)
        db.session.commit()
       


    if exist_upvote:
       return jsonify({'message': 'you already upvoted this answer'})
       

    # create new upvote
    upvote = UpVote(user_id=user_id, answer_id=answer.id)
    db.session.add(upvote)
    db.session.commit()

    return jsonify({'message': 'upvoted successfully'})

@app.route('/votes/downvote/<int:answer_id>', methods=['POST'])
def vote_down(answer_id):
    # get answer by id
    answer = Answer.query.get(answer_id)

    if not answer:
        return jsonify({'error': "answer not found"})

    user_id = request.json.get('user_id')

    # check if user has already voted
    exist_upvote = UpVote.query.filter_by(user_id=user_id, answer_id=answer.id).first()
    exist_downvote = DownVote.query.filter_by(user_id=user_id, answer_id=answer.id).first()

    if exist_downvote:
        return jsonify({'message': 'you already downvoted this answer'})

    if exist_upvote:
        # delete upvote
        db.session.delete(exist_upvote)
        db.session.commit()

    # create new downvote
    downvote = DownVote(user_id=user_id, answer_id=answer.id)
    db.session.add(downvote)
    db.session.commit()

    return jsonify({'message': 'downvoted successfully'})

@app.route('/votes/user/<int:user_id>', methods=['GET'])
def get_user_votes(user_id):
    upvotes = UpVote.query.filter_by(user_id=user_id).all()
    upvote_list = [vote.to_dict() for vote in upvotes]
    downvotes = DownVote.query.filter_by(user_id=user_id).all()
    downvote_list = [vote.to_dict() for vote in downvotes]

    # calculate the total number of upvotes and downvotes for the user
    total_upvotes = len(upvotes)
    total_downvotes = len(downvotes)

    return jsonify({'upvotes': upvote_list, 'downvotes': downvote_list, 'total_upvotes': total_upvotes, 'total_downvotes': total_downvotes})


if __name__ == '__main__':
    with app.app_context():  
        db.create_all()  
    app.run(debug=True)

