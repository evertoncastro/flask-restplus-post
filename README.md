# Flask RESTPlus Post

Projeto criado como exemplo de implementação do post *API com Flask RESTPlus* em https://evertoncastro.com

Todos os comando abaixo devem ser executados no diretório raiz do projeto.

#### Preparando ambiente virtual
```
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

#### Instalando bibliotecas
```
pip install -r app/requirements.txt
```

### Definindo variáveis de ambiente
```
export PYTHONPATH=$PYTHONPATH:$(pwd)/app
export FLASK_ENV=development
export FLASK_APP=app/main.py
```

#### Criação de banco e tabelas
```
flask db init --directory=development_migrations (esse comando cria o banco de dados)
flask db migrate --directory=development_migrations
flask db upgrade --directory=development_migrations
```

### Executando os tests
```
python tests/runner.py
```

### Iniciando a aplicação
```
flask run
```

Se tudo der certo acesse: [http://127.0.0.1:5000/podcast_api/v1.0/](http://127.0.0.1:5000/podcast_api/v1.0/)

