from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import config_options
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# app initialization
app = Flask(__name__)
# app configurations
app.config.from_object(config_options['dev_config'])
# database initialization
db = SQLAlchemy(app)
# bootstrap initialization
Bootstrap(app)
# flask mail initialization
mail = Mail(app)
# bcrypt initialization
bcrypt = Bcrypt(app)
# set up flask login
login_manager = LoginManager(app)
# add a route that a page defaults to if the user is not logged in
login_manager.login_view = 'login' # this is the function name of our route

# other imports that depend on the variables above
from app import views
from app import models