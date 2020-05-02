import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    Debug = True


class DevelopmentConfig(Config):
    ...


development = DevelopmentConfig()
