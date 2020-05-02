import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    Debug = True


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


development = DevelopmentConfig()
testing = TestingConfig()
