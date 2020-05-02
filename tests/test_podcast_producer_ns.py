from unittest import TestCase
from main import app
from app import db
from tests.runner import clear_database
from models import Producer
from json import loads


class TestProducerNamespace(TestCase):

    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.client = app.test_client()
        self.db = db
        self.session = self.db.session

        clear_database(self.db)

    def tearDown(self):
        clear_database(self.db)

    def testa_se_retorna_400_para_parametros_vazios(self):
        response = self.client.post(
            '/podcast_api/v1.0/produtor/cria',
            json={}
        )
        self.assertEqual(response.status_code, 400)

    def testa_se_retorna_400_para_nome_vazio(self):
        response = self.client.post(
            '/podcast_api/v1.0/produtor/cria',
            json={'name': None}
        )
        self.assertEqual(response.status_code, 400)

    def testa_se_cria_produtor_no_banco_e_retorna_200(self):
        response = self.client.post(
            '/podcast_api/v1.0/produtor/cria',
            json={'name': 'Produtor 1'}
        )
        data = loads(response.get_data())
        producer = Producer().fetch(self.session, data['id'])
        self.assertIsNotNone(producer)
        self.assertEqual(response.status_code, 200)

    def testa_se_retorna_um_produtor_que_existe_no_banco(self):
        Producer().create(self.session, name='Produtor 1')
        self.session.commit()
        response = self.client.get(
            '/podcast_api/v1.0/produtor/1'
        )
        self.assertEqual(response.status_code, 200)
        data = loads(response.get_data())
        self.assertEquals(data, {
            'id': 1,
            'name': 'Produtor 1'
        })

    def testa_se_retorna_404_quando_id_nao_existe(self):
        response = self.client.get(
            '/podcast_api/v1.0/produtor/1'
        )
        self.assertEqual(response.status_code, 404)

    def testa_se_a_lista_de_produtores_que_esta_no_banco(self):
        Producer().create(self.session, name='Produtor 1')
        Producer().create(self.session, name='Produtor 2')
        Producer().create(self.session, name='Produtor 3')
        self.session.commit()
        response = self.client.get(
            '/podcast_api/v1.0/produtor/todos'
        )
        self.assertEqual(response.status_code, 200)
        data = loads(response.get_data())
        self.assertEquals(len(data['list']), 3)

    def testa_se_remove_um_produtor_do_banco_de_dados(self):
        Producer().create(self.session, name='Produtor 1')
        self.session.commit()
        response = self.client.delete(
            '/podcast_api/v1.0/produtor/remove/1'
        )
        self.assertEqual(response.status_code, 200)
