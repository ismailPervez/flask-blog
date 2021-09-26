from app import app
from flask import render_template

'''
this is the home route - where the user first lands 
'''
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/articles')
def get_articles():
    return render_template('articles.html')