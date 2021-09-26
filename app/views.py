from app import app, db, mail, bcrypt
from flask import render_template, url_for, redirect, flash, request
from app.forms import RegistrationForm, CreatePost, LoginForm
from flask_mail import Message
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

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

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # check if the url has a parameter - next
            next_route = request.args.get('next')
            login_user(user)
            # print("successfully logged in as: ", current_user.username)
            flash(f'successfully logged in as {current_user.username}', 'success')
            return redirect(next_route) if next_route else redirect(url_for('home'))

        flash('login unsuccessful, please check the username or password', 'danger')

    
    return render_template('login.html', form=form)

# route for logging out user
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

'''
user's account/profile page
'''
@app.route('/account')
@login_required
def get_account():
    return render_template('account.html')


@app.route("/create", methods=["GET", "POST"])
def create():
    form = CreatePost()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        # the tags need to be JSON serializable before we store them in the database
        tags = form.tags.data.split(' ')
        # initial upvotes and downvotes are 0
        post = Post(
            title=title,
            content=content,
            tags=str(tags),
            upvotes=0,
            downvotes=0,
            user_id=current_user.id
        )

        db.session.add(post)
        db.session.commit()

        flash('post created successfully', 'success')
        return redirect(url_for("account"))

    else:
        print('not validated')

    return render_template("createpost.html", form=form)