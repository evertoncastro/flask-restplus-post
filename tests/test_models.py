from unittest import TestCase
from models import Producer
from models import Episode
from app import db
from tests.runner import clear_database


class TestProducerModel(TestCase):

    def setUp(self):
        self.db = db
        self.session = self.db.session
        self.db.create_all()

    def tearDown(self):
        self.session.close()
        clear_database(self.db)

    def testa_se_cria_produtor_com_sucesso(self):
        novo_produtor = Producer().create(self.session, name='Produtor 1')
        self.session.commit()
        teste_produtor = self.session.query(Producer).filter_by(id=novo_produtor.id).first()
        self.assertIsNotNone(teste_produtor)

    def testa_se_busca_produtor_que_existe_no_banco(self):
        novo_produtor = Producer().create(self.session, name='Produtor 1')
        self.session.commit()
        teste_produtor = Producer().fetch(self.session, novo_produtor.id)
        self.assertIsNotNone(teste_produtor)
        self.assertEqual(teste_produtor.name, 'Produtor 1')

    def testa_se_busca_todos_produtores_no_banco(self):
        Producer().create(self.session, name='Produtor 1')
        Producer().create(self.session, name='Produtor 2')
        Producer().create(self.session, name='Produtor 3')
        self.session.commit()
        produtores = Producer().fetch_all(self.session)
        self.assertEqual(len(produtores), 3)

    def testa_se_remove_um_produtor_do_banco(self):
        novo_produtor = Producer().create(self.session, name='Produtor 1')
        self.session.commit()
        teste_produtor = Producer().fetch(self.session, novo_produtor.id)
        self.assertIsNotNone(teste_produtor)
        apagado = Producer().delete(self.session, teste_produtor.id)
        self.session.commit()
        self.assertTrue(apagado)
        teste_produtor = Producer().fetch(self.session, novo_produtor.id)
        self.assertIsNone(teste_produtor)


class TestEpisodeModel(TestCase):

    def setUp(self):
        self.db = db
        self.session = self.db.session
        self.db.create_all()

    def tearDown(self):
        self.session.close()
        clear_database(self.db)

    def testa_se_cria_episodio_com_sucesso(self):
        novo_episodio = Episode().create(
            self.session,
            producer_id=1,
            name='Episódio 1',
            url='http://produtor/episodio/1'
        )
        self.session.commit()
        teste_episodio = self.session.query(Episode).filter_by(id=novo_episodio.id).first()
        self.assertIsNotNone(teste_episodio)

    def testa_se_busca_episodio_que_existe_no_banco(self):
        novo_episodio = Episode().create(
            self.session,
            producer_id=1,
            name='Episódio 1',
            url='http://produtor/episodio/1'
        )
        self.session.commit()
        teste_episodio = Episode().fetch(self.session, 1, novo_episodio.id)
        self.assertIsNotNone(teste_episodio)

    def testa_se_busca_episodios_de_um_produtor(self):
        Episode().create(
            self.session,
            producer_id=1,
            name='Episódio 1',
            url='http://produtor/episodio/1'
        )
        Episode().create(
            self.session,
            producer_id=1,
            name='Episódio 2',
            url='http://produtor/episodio/2'
        )
        Episode().create(
            self.session,
            producer_id=1,
            name='Episódio 3',
            url='http://produtor/episodio/3'
        )
        self.session.commit()
        episodios = Episode().fetch_all(self.session)
        self.assertEqual(len(episodios), 3)

    def testa_se_remove_episodio_de_um_produtor(self):
        novo_episodio = Episode().create(
            self.session,
            producer_id=1,
            name='Episódio 1',
            url='http://produtor/episodio/1'
        )
        self.session.commit()
        teste_episodio = Episode().fetch(self.session, 1, novo_episodio.id)
        self.assertIsNotNone(teste_episodio)
        apagado = Episode().delete(self.session, 1, teste_episodio.id)
        self.session.commit()
        self.assertTrue(apagado)
        teste_produtor = Episode().fetch(self.session, 1, teste_episodio.id)
        self.assertIsNone(teste_produtor)
