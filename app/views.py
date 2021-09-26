from app import app
from flask import render_template

'''
this is the home route - where the user first lands 
'''
@app.route('/')
def home():
    return render_template('home.html')

'''
this route will get the latest post in each category
'''
@app.route('/articles')
def get_articles():
    return render_template('articles.html')

'''
if the user wants to sign up - accepts both GET and POST methods 
'''
@app.route('/register', methods=["GET", "POST"])
def sign_up():
    return render_template('register.html')

