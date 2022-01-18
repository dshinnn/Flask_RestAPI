from app import app
from flask import render_template
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
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        print(username, email, password)
    return render_template('register.html', form=form)