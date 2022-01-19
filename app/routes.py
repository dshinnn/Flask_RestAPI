from app import app
from flask import render_template, redirect, url_for
from app.forms import RegisterForm, LoginForm
from app.models import User

@app.route('/')
def index():
    colors = ['red', 'blue', 'green']
    person = {
        'name': 'Ferris Buller',
        'age': 18,
        'best_friend': 'Cameron'
    }
    return render_template('index.html', name='David', city='Arcadia', colors=colors, person=person)

@app.route('/name')
def name():
    return render_template('name.html', name='David')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    # checks if the method is a post and if it is, it checks if all inputs are valid
    if form.validate_on_submit():
        # Get data from the form
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        # Check if either the username or email is already in db
        user_exists = User.query.filter((User.username==username)|(User.email==email)).all()
        if user_exists:
            return redirect(url_for('register'))

        # Create a new user instance using form data
        User(username=username, email=email, password=password)

        # Redirects to home page after registration
        return redirect(url_for('index'))
        
    return render_template('register.html', form=form)

@app.route('/login')
def login():
    form = LoginForm()

    return render_template('login.html', form=form)