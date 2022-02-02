from flask import jsonify, request
from app.models import User, Product
from . import bp as api
from .auth import basic_auth, token_auth
from datetime import datetime

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
@api.route('/user/<int:id>', methods=['PUT'])
@token_auth.login_required
def updated_user(id):
    current_user = token_auth.current_user()
    if current_user.id != id:
        return jsonify({'error': 'You do not have access to update this user.'}), 403
    user = User.query.get_or_404(id)
    data = request.json
    user.update(data)
    return jsonify(user.to_dict())

# Delete an user by id
@api.route('/user/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    current_user = token_auth.current_user()
    if current_user.id != id:
        return jsonify({'error': 'You do not have access to delete this user.'}), 403
    
    User.query.get_or_404(id).delete()
    return jsonify({}), 204

# Get all products
@api.route('/products')
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

# Get single product
@api.route('/products/<int:id>')
def get_product(id):
    product = Product.query.get_or_404(id)
    if product:
        return jsonify(product.to_dict())

# Create product
@api.route('/products', methods=['POST'])
def create_product():
    data = request.json
    print(data)

    # Validating data
    for field in ['name', 'price', 'image_url', 'category_id']:
        if field not in data:
            return jsonify({'error': f'Missing {field} field'})

    # Grabs field data from body of the POST request
    name = data['name']
    price = data['price']
    image_url = data['image_url']
    category_id = data['category_id']

    # Creates new product using retrieved data
    new_product = Product(name=name, price=price, image_url=image_url, category_id=category_id)
    
    # Returns a print out of the product
    return jsonify(new_product.to_dict())

# Update product
@api.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json
    product.update(data)
    return(product.to_dict())

# Delete product