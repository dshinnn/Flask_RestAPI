from app import app
from flask import render_template

@app.route('/')
def index():
    my_name = 'David'
    colors = ['red', 'blue', 'green']
    person = {
        'name': 'Ferris Buller',
        'age': 18,
        'best_friend': 'Cameron'
    }
    return render_template('index.html', name = 'David', city='Arcadia', colors=colors, person=person)


@app.route('/name')
def name():
    my_name = 'David'
    return render_template('name.html', name='David')


@app.route('/test')
def test_name():
    return '<h1>This is a test</h1>'