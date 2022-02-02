from flask import jsonify
from app.models import User
from . import bp as api

@api.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@api.route('/users/<id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())