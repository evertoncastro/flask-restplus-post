from app import app
from api.podcast import load_api as load_podcast_api

# Aplicativo Flask fazendo o carregamento da API
load_podcast_api(app)

if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])
