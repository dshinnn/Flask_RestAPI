from app import app
from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required
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
@login_required
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Get data from the form
        username = form.username.data
        password = form.password.data

        # Query user table for user with username
        user = User.query.filter_by(username=username).first()

        # if the user does not exist or the user has an incorrect password
        if not user or not user.check_password(password):
            # redirect to login page
            return redirect(url_for('login'))
        # if user does exist and correct password, log user in
        login_user(user)
        print('User has been logged in')
        return redirect(url_for('index'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))