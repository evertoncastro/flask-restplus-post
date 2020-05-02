from app import db
from flask_restplus import Api
from flask_restplus import Namespace, Resource, fields
from models import Producer
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import InternalServerError

namespace = Namespace('produtor', description='Produtor')

create_producer_request = namespace.model('Dados para criação de produtor', {
    'name': fields.String(required=True, description='Nome do produtor')
})

create_producer_response = namespace.model('Resposta da criaçao de produtor', {
    'id': fields.Integer(required=True, description='Identificador único do produtor')
})

get_producer_response = namespace.model('Resposta pegar produtor', {
    'id': fields.Integer(required=True, description='Identificador único do produtor'),
    'name': fields.String(required=True, description='Nome do produtor')
})

list_producers = namespace.model('Lista de produtores', {
    'id': fields.Integer(required=True, description='Identificador único do produtor'),
    'name': fields.String(required=True, description='Nome do produtor')
})

list_producers_response = namespace.model('Resposta da lista de produtores', {
    'list': fields.Nested(list_producers, required=True, description='Lista de produtores')
})

delete_producer_response = namespace.model('Resposta da remocao de produtores', {
    'removed': fields.Boolean(required=True, description='Indicador de remocao com sucesso')
})

headers = namespace.parser()
# Aqui podemos adicionar mais parametros


@namespace.route('/cria', doc={"description": 'Cria um novo produtor'})
@namespace.expect(headers)
class CreateProducer(Resource):
    @namespace.response(200, 'Success')
    @namespace.response(400, 'Request Error')
    @namespace.response(500, 'Server Error')
    @namespace.expect(create_producer_request, validate=True)
    @namespace.marshal_with(create_producer_response)
    def post(self):
        """Cria novo produtor"""
        session = db.session
        try:
            producer = Producer().create(session, name=namespace.payload['name'])
            session.commit()
            return {'id': producer.id}
        except Exception as e:
            raise InternalServerError(e.args[0])
        finally:
            session.close()


@namespace.route('/<int:id>', doc={"description": 'Pega produtor'})
@namespace.param('id', 'Identificador único do produtor')
@namespace.expect(headers)
class GetProducer(Resource):
    @namespace.response(200, 'Success')
    @namespace.response(404, 'Not Found Error')
    @namespace.response(500, 'Server Error')
    @namespace.marshal_with(get_producer_response)
    def get(self, id):
        """Pega produtor"""
        session = db.session
        try:
            producer = Producer().fetch(session, id)
            if not producer:
                raise NotFound('Not found producer')
            return producer
        except HTTPException as e:
            raise e
        except Exception as e:
            raise InternalServerError(e.args[0])
        finally:
            session.close()


@namespace.route('/todos', doc={"description": 'Lista todos os produtor'})
@namespace.expect(headers)
class ListProducers(Resource):
    @namespace.response(200, 'Success')
    @namespace.response(404, 'Not Found Error')
    @namespace.response(500, 'Server Error')
    @namespace.marshal_with(list_producers_response)
    def get(self):
        """Lista todos os produtores"""
        session = db.session
        try:
            producers = Producer().fetch_all(session)
            return {'list': producers}
        except HTTPException as e:
            raise e
        except Exception as e:
            raise InternalServerError(e.args[0])
        finally:
            session.close()


@namespace.route('/remove/<int:id>', doc={"description": 'Apaga produtor'})
@namespace.param('id', 'Identificador único do produtor')
@namespace.expect(headers)
class DeleteProducers(Resource):
    @namespace.response(200, 'Success')
    @namespace.response(500, 'Server Error')
    @namespace.marshal_with(delete_producer_response)
    def delete(self, id):
        """Remove produtor"""
        session = db.session
        try:
            removed = Producer().delete(session, id)
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
