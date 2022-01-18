import os 

class Config(object):
    SECRET_KEY='440d499641413a010b22b09fcb378c8562e1aa74f8e83ae2f5edfc69b8e57e23'#os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI='sqlite:///site.db'
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')

class DevConfig(Config):
    DEBUG=True

class ProdConfig(Config):
    pass

config_options = {
    "dev_config": DevConfig,
    "prod_config": ProdConfig
}