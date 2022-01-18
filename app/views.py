import flask
from app import app, db, mail, bcrypt
from flask import render_template, url_for, redirect, flash, request
from app.forms import RegistrationForm, CreatePost, LoginForm, UpdatePost
from flask_mail import Message
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import ast
import requests
'''
this is the home route - where the user first lands 
'''
@app.route('/')
def home():
    # get random quote
    quote = requests.get('http://quotes.stormconsultancy.co.uk/random.json')
    quote_in_json = quote.json()
    post = Post.query.order_by(Post.id.desc()).limit(3).all()
    latest_posts = []
    users = []
    for post in post:

        user = User.query.filter_by(id=post.user_id).first()
        users.append(user)

        post = Post(
            id=post.id,
            title=post.title,
            content=post.content,
            upvotes=post.upvotes,
            downvotes=post.downvotes,
            tags=post.tags,
            user_id=post.user_id
        )
        post.tags = ast.literal_eval(post.tags)
        latest_posts.append(post)

    return render_template('home.html', posts=latest_posts, users=users, quote=quote_in_json)

'''
this route will get the latest post in each category
'''
@app.route('/articles')
def get_articles():
    # get latest python posts
    python_posts = Post.query.order_by(Post.id.desc()).limit(15).all()

    latest_python_posts = []
    python_posts_users = []
    for post in python_posts:
        post = Post(
            id=post.id,
            title=post.title,
            content=post.content,
            upvotes=post.upvotes,
            downvotes=post.downvotes,
            tags=post.tags,
            user_id=post.user_id
        )
        post.tags = ast.literal_eval(post.tags)
        print(post.tags)

        if 'python' in post.tags or 'pythonprogramming' in post.tags or 'pythoneer' in post.tags:
            print('its a python post')
            latest_python_posts.append(post)
            user = User.query.filter_by(id=post.user_id).first()
            python_posts_users.append(user)

    if len(latest_python_posts) > 3:
        latest_python_posts = latest_python_posts[:3]
        python_posts_users = python_posts_users[:3]

    # get latest js posts
    js_posts = Post.query.order_by(Post.id.desc()).limit(15).all()

    latest_js_posts = []
    js_posts_users = []
    for post in js_posts:
        post = Post(
            id=post.id,
            title=post.title,
            content=post.content,
            upvotes=post.upvotes,
            downvotes=post.downvotes,
            tags=post.tags,
            user_id=post.user_id
        )
        post.tags = ast.literal_eval(post.tags)
        print(post.tags)

        if 'js' in post.tags or 'javascript' in post.tags or 'ES6' in post.tags:
            print('its a python post')
            latest_js_posts.append(post)
            user = User.query.filter_by(id=post.user_id).first()
            js_posts_users.append(user)

    if len(latest_js_posts) > 3:
        latest_js_posts = latest_js_posts[:3]
        js_posts_users = js_posts_users[:3]

    return render_template('articles.html', python_posts=latest_python_posts, python_posts_users=python_posts_users, js_posts=latest_js_posts, js_posts_users=js_posts_users)

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
    user = User.query.filter_by(username=current_user.username).first()
    all_posts = user.posts
    
    total_upvote_count = 0
    total_downvote_count = 0
    for post in all_posts:
        # this method converts a string representation of a list into a list
        post.tags = ast.literal_eval(post.tags)
        total_upvote_count += post.upvotes
        total_downvote_count += post.downvotes

    return render_template('account.html', posts=all_posts, upvotes=total_upvote_count, downvotes=total_downvote_count)


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
        return redirect(url_for("get_account"))

    return render_template("createpost.html", form=form)


'''
view to delete each post
'''
@app.route('/delete/<int:post_id>', methods=["GET", "DELETE"])
def delete_post(post_id):
    # check if the post belongs to the current user before deleting it
    post = Post.query.filter_by(id=post_id).first()
    if current_user.id == post.user_id:
        db.session.delete(post)
        db.session.commit()
        flash('post deleted successfully', 'success')
    return redirect(url_for('get_account'))

# update a post - when liked or disliked
@app.route('/update/<int:post_id>', methods=['PUT'])
@login_required
def update_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if "upvotes" in request.json:
        post.upvotes = request.json["upvotes"]

    if "downvotes" in request.json:
        post.downvotes = request.json["downvotes"]

    db.session.commit()

    return "status: ok"

# each blog post
@app.route('/full-post/<int:post_id>')
def get_post(post_id):
    post = Post.query.filter_by(id=post_id).first()

    return render_template('post.html', post=post)

# update post
@app.route('/update/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post_content(post_id):
    post = Post.query.get(post_id)
    form = UpdatePost()
    # default values when loading
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        tags = ' '.join(ast.literal_eval(post.tags))
        form.tags.data = tags

        return render_template('updatepost.html', form=form)

    else:
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            # the tags need to be JSON serializable before we store them in the database
            tags = str(form.tags.data.split(' '))
            post.title = title
            post.content = content
            post.tags = tags

            db.session.commit()

            flash('post updated successfully', 'success')

            return render_template('updatepost.html', form=form)
