from users_api.app import create_app
from users_api.config import Config

app = create_app(config_object=Config)

@app.route('/')
def hello():
    return 'Hello world'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)