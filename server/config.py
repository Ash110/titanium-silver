import os

class Config(object):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    INPUT_FOLDER = os.getcwd()+'/server/flaskr/codes/Input'

    OUTPUT_FOLDER = os.getcwd()+'/server/flaskr/codes/Output'
    
class DevelopmentConfig(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD=True
    INPUT_FOLDER = os.getcwd()+'/server/flaskr/codes/Input'

    OUTPUT_FOLDER = os.getcwd()+'/server/flaskr/codes/Output'


class TestingConfig(Config):
    TESTING = True