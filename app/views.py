from app import app, db, mail, bcrypt
from flask import render_template, url_for, redirect, flash
from app.forms import RegistrationForm, CreatePost, LoginForm
from flask_mail import Message
from app.models import User, Post

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
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = hashed_password
        )

        db.session.add(user)
        db.session.commit()

        # print("account created successfully!")
        flash('account created successfully', 'success')

        msg = Message("welcome to club review", sender="noreply@clubreview.com", recipients=[form.email.data])
        msg.html = f'''
            <h1>welcome to club review</h1>
            <p>Hi {form.username.data},</p>
            <p>welcome to club review. thanks for joining our ever growing society</p>
        '''
        
        mail.send(msg)
        return redirect(url_for('home')) # you pass in the view function name and not the 
        # route name

    return render_template('register.html', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

