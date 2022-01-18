from app import app
from flask import render_template, redirect, url_for
from app.forms import RegisterForm

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
        username = form.username.data
        email = form.email.data
        password = form.password.data
        print(username, email, password)
        return redirect(url_for('index'))
        
    return render_template('register.html', form=form)