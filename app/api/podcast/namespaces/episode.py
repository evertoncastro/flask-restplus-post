from app import db
from flask_restplus import Api
from flask_restplus import Namespace, Resource, fields
from models import Episode
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import InternalServerError

namespace = Namespace('episodio', description='Episódio')

create_episode_request = namespace.model('Dados para criação de episódio', {
    'producer_id': fields.Integer(required=True, description='Identificador do produtor'),
    'name': fields.String(required=True, description='Nome do episódio'),
    'url': fields.String(required=True, description='Url do episódio')
})

create_episode_response = namespace.model('Resposta da criaçao de episódio', {
    'id': fields.Integer(required=True, description='Identificador único do episódio')
})

get_episode_response = namespace.model('Resposta pegar episódio', {
    'id': fields.Integer(required=True, description='Identificador único do episódio'),
    'name': fields.String(required=True, description='Nome do episódio'),
    'url': fields.String(required=True, description='Url do episódio')
})

list_episodes = namespace.model('Lista de episódios', {
    'id': fields.Integer(required=True, description='Identificador único do episódio'),
    'name': fields.String(required=True, description='Nome do episódio'),
    'url': fields.String(required=True, description='Url do episódio')
})

list_episodes_response = namespace.model('Resposta da lista de episódios', {
    'list': fields.Nested(list_episodes, required=True, description='Lista de episódios')
})

delete_episode_response = namespace.model('Resposta da remocao de episódio', {
    'removed': fields.Boolean(required=True, description='Indicador de remocao com sucesso')
})

headers = namespace.parser()
# Aqui podemos adicionar mais parametros


@namespace.route('/cria', doc={"description": 'Cria um novo episódio'})
@namespace.expect(headers)
class CreateEpisode(Resource):
    @namespace.response(200, 'Success')
    @namespace.response(400, 'Request Error')
    @namespace.response(500, 'Server Error')
    @namespace.expect(create_episode_request, validate=True)
    @namespace.marshal_with(create_episode_response)
    def post(self):
        """Cria novo episódio"""
        session = db.session
        try:
            episode = Episode().create(
                session,
                producer_id=namespace.payload['producer_id'],
                name=namespace.payload['name'],
                url=namespace.payload['url']
            )
            session.commit()
            return {'id': episode.id}
        except Exception as e:
            raise InternalServerError(e.args[0])
        finally:
            session.close()


@namespace.route('/<int:producer_id>/<int:id>', doc={"description": 'Pega episódio'})
@namespace.param('producer_id', 'Identificador único do produtor')
@namespace.param('id', 'Identificador único do episódio')
@namespace.expect(headers)
class GetEpisode(Resource):
    @namespace.response(200, 'Success')
    @namespace.response(404, 'Not Found Error')
    @namespace.response(500, 'Server Error')
    @namespace.marshal_with(get_episode_response)
    def get(self, producer_id, id):
        """Pega episódio"""
        session = db.session
        try:
            producer = Episode().fetch(session, producer_id, id)
            if not producer:
                raise NotFound('Not found producer')
            return producer
        except HTTPException as e:
            raise e
        except Exception as e:
            raise InternalServerError(e.args[0])
        finally:
            session.close()


@namespace.route('/todos', doc={"description": 'Lista todos os episódios'})
@namespace.expect(headers)
class ListEpisodes(Resource):
    @namespace.response(200, 'Success')
    @namespace.response(404, 'Not Found Error')
    @namespace.response(500, 'Server Error')
    @namespace.marshal_with(list_episodes_response)
    def get(self):
        """Lista todos os episódios"""
        session = db.session
        try:
            episodes = Episode().fetch_all(session)
            return {'list': episodes}
        except HTTPException as e:
            raise e
        except Exception as e:
            raise InternalServerError(e.args[0])
        finally:
            session.close()


@namespace.route('/remove/<int:producer_id>/<int:id>',
                 doc={"description": 'Apaga episódio'})
@namespace.param('producer_id', 'Identificador único do produtor')
@namespace.param('id', 'Identificador único do episódio')
@namespace.expect(headers)
class DeleteProducers(Resource):
    @namespace.response(200, 'Success')
    @namespace.response(500, 'Server Error')
    @namespace.marshal_with(delete_episode_response)
    def delete(self, producer_id, id):
        """Remove episódio"""
        session = db.session
        try:
            removed = Episode().delete(session, producer_id, id)
            session.commit()
            return {'removed': removed}
        except Exception as e:
            raise InternalServerError(e.args[0])
        finally:
            session.close()


def bind_with_api(api: Api):
    """
    Adiciona o namespace à API recebida
    :param api: Flask Restplus API
    :return: Vazio
    """
    api.add_namespace(namespace)
    return None
