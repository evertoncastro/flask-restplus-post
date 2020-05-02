import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    Debug = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTPLUS_MASK_HEADER = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')


development = DevelopmentConfig()
testing = TestingConfig()
