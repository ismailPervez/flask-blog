from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import config_options

# app initialization
app = Flask(__name__)
# app configurations
app.config.from_object(config_options['dev_config'])
