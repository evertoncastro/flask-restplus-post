import os
import sys
from unittest.loader import TestLoader
from unittest import TextTestRunner
from app import app
from app import db


def test_suite():
    # A abertura de contexto faz o banco de dados estar pronto para todos os casos de teste
    # Isso nos poupará de ter que fazer a configuração em cada classe de testes
    with app.app_context():
        try:
            os.remove('app/test.db')
        except IOError:
            pass
        db.create_all()
        # O Test Loader vai procurar e executar testes em todos os arquivos que tenham o padrão test_*
        suite = TestLoader().discover(
            'tests',
            pattern='test_*.py',
            top_level_dir=os.environ['PYTHONPATH'].split(os.pathsep)[0]
        )
        return TextTestRunner(verbosity=1).run(suite)


def clear_database(_db):
    # Remove todas as tabelas do banco para o contexto de teste
    db.session.rollback()
    for table in reversed(_db.metadata.sorted_tables):
        _db.session.execute(table.delete())
    _db.session.commit()


if __name__ == '__main__':
    result = test_suite()
    if not result.wasSuccessful():
        sys.exit(1)
