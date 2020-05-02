from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


def setup_app() -> object:
    """
    Creates a new Flask application
    :rtype: Flask object
    """
    _app = Flask(__name__)
    _app.config.from_object(
        f"config.{getenv('FLASK_ENV', 'development')}"
    )
    return _app


def setup_database(_app: object) -> SQLAlchemy:
    """
    Adiciona um novo banco de dados ao aplicativo Flask
    :param _app: Aplicativo Flask
    :return: Novo banco de dados criado
    """
    _db = SQLAlchemy()
    _db.init_app(_app)
    return _db


def setup_database_migration(_app: object, _db: SQLAlchemy) -> Migrate:
    """
    Cria a migração de estrutura do banco de dados
    :param _app: Aplicativo Flask
    :param _db: Banco de dados
    :return: O objeto de migração
    """
    return Migrate(_app, _db)


app = setup_app()
db = setup_database(app)
migrate = setup_database_migration(app, db)
