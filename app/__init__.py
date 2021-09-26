from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import config_options
from flask_bootstrap import Bootstrap
from flask_mail import Mail

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

# other imports that depend on the variables above
from app import views
from app import models