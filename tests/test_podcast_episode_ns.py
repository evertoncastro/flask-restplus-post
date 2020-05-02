from unittest import TestCase
from main import app
from app import db
from tests.runner import clear_database
from models import Episode
from json import loads


class TestEpisodeNamespace(TestCase):

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
            '/podcast_api/v1.0/episodio/cria',
            json={}
        )
        self.assertEqual(response.status_code, 400)

    def testa_se_retorna_400_para_nome_vazio(self):
        response = self.client.post(
            '/podcast_api/v1.0/episodio/cria',
            json={'name': None}
        )
        self.assertEqual(response.status_code, 400)

    def testa_se_cria_episodio_no_banco_e_retorna_200(self):
        response = self.client.post(
            '/podcast_api/v1.0/episodio/cria',
            json={
                'producer_id': 1,
                'name': 'Produtor 1',
                'url': 'http://produtor1/episodio1'
            }
        )
        data = loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        producer = Episode().fetch(self.session, 1, data['id'])
        self.assertIsNotNone(producer)

    def testa_se_retorna_um_episodio_que_existe_no_banco(self):
        Episode().create(
            self.session,
            producer_id=1, name='Episódio 1', url='/')
        self.session.commit()
        response = self.client.get(
            '/podcast_api/v1.0/episodio/1/1'
        )
        self.assertEqual(response.status_code, 200)
        data = loads(response.get_data())
        self.assertEquals(data, {
            'id': 1,
            'name': 'Episódio 1',
            'url': '/'
        })

    def testa_se_retorna_404_quando_id_do_episodio_nao_existe(self):
        response = self.client.get(
            '/podcast_api/v1.0/episodio/1/1'
        )
        self.assertEqual(response.status_code, 404)

    def testa_se_a_lista_de_produtores_que_esta_no_banco(self):
        Episode().create(
            self.session,
            producer_id=1, name='Episódio 1', url='/')
        Episode().create(
            self.session,
            producer_id=2, name='Episódio 1', url='/')
        self.session.commit()
        response = self.client.get(
            '/podcast_api/v1.0/episodio/todos'
        )
        self.assertEqual(response.status_code, 200)
        data = loads(response.get_data())
        self.assertEquals(len(data['list']), 2)

    def testa_se_remove_um_produtor_do_banco_de_dados(self):
        Episode().create(
            self.session,
            producer_id=1, name='Episódio 1', url='/')
        self.session.commit()
        response = self.client.delete(
            '/podcast_api/v1.0/episodio/remove/1/1'
        )
        self.assertEqual(response.status_code, 200)
