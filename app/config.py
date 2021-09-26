import os 

class Config(object):
    SECRET_KEY=os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI='sqlit:///site.db'

class DevConfig(Config):
    DEBUG=True

class ProdConfig(Config):
    pass

config_options = {
    "dev_config": DevConfig,
    "prod_config": ProdConfig
}