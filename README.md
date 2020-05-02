# Flask RESTPlus Post

Projeto criado como exemplo de implementação do post *API com Flask RESTPlus* em https://evertoncastro.com

### Ambiente de desenvolvimento
```
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

### Dependências

```
pip install -r app/requirements.txt
```

### Variáveis de ambiente
```
export PYTHONPATH=$PYTHONPATH:$(pwd)/app
export FLASK_ENV=development
export FLASK_APP=app/main.py
```

### Iniciano a aplicação
```
flask run
```