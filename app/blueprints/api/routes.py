from flask import jsonify, request
from app.models import User
from . import bp as api
from .auth import basic_auth, token_auth

# Get token
@api.route('/token', methods=['POST'])
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    token = user.get_token()
    return jsonify({'token': token})

# Get all users
@api.route('/users')
@token_auth.login_required
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Get a single user by id
@api.route('/users/<id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

# Create an user
@api.route('/users', methods=['POST'])
def create_user():
    data = request.json
    print(data)
    
    # Validate data
    for field in ['username', 'email', 'password']:
        if field not in data:
            return jsonify({'error': f'You are missing the {field} field'}), 400

    # Grab data from the request body
    username = data['username']
    email = data['email']
    password = data['password']

    # Checks if user exists
    user_exists = User.query.filter((User.username==username)|(User.email==email)).all()

    if user_exists:
        return jsonify({'error': f'Username with { username } already or email with { email } already exists'}), 400
    
    # Create new user
    # new_user = User(username=username, email=email, password=password)
    new_user = User(**data)     # does the same thing as the code above

    return jsonify(new_user.to_dict())

# Update an user by id
@api.route('/user/<id>', methods=['PUT'])
@token_auth.login_required
def updated_user(id):
    pass

# Delete an user by id
@api.route('/user/<id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    pass