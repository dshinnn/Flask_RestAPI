import os
import base64
from sqlalchemy import ForeignKey
from app import db, login
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def get_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(32), unique=True, index=True)
    token_expiration = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<User|{self.username}>'

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'date_created': self.date_created,
            'is_admin': self.is_admin
        }

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        
        if self.token and self.token_expiration > now + timedelta(minutes=1):
            return self.token
        
        # Generates a new random token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)

        # Save to database
        db.session.commit()
        
        return self.token

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self, data):
        for field in data:
            if field not in {'username', 'email', 'is_admin'}:
                continue
            if field == 'password':
                setattr(self, field, generate_password_hash(data[field]))
            else:
                setattr(self, field, data[field])
        db.session.commit()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    color = db.Column(db.String(20), nullable=False)
    products = db.relationship('Product', backref='category')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()


    def __repr__(self):
        return f'<Category|{self.name}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    name = db.Column(db.String(180), nullable=False)
    price = db.Column(db.Numeric(5,2), nullable=False)
    image_url = db.Column(db.String(256))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Product|{self.name}>'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "image_url": self.image_url,
            "date_created": self.date_created
        }

    def update(self, data):
        for field in data:
            if field not in {'name', 'price', 'image_url', 'date_created'}:
                continue
            setattr(self, field, data[field])
        db.session.commit()

    def save(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()