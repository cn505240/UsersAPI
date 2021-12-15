from users_api.app import create_app
from users_api.config import Config

app = create_app(config_object=Config)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)