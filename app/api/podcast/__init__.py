from flask import Blueprint
from flask_restplus import Api as ApiRestPlus

api = ApiRestPlus(
    Blueprint('API de PodCasts', __name__),
    title='API para gestão de podcasts',
    version='1.0',
    description='Endpoints para gestão de produtores e episódios de podcasts'
)


def load_api(app) -> object:
    """
    Este método serve para o aplicativo Flask carregar a API em si
    :param app: Aplicativo Flask
    :return: Vazio
    """
    app.register_blueprint(api.blueprint, url_prefix='/podcast_api/v1.0')
    return None
