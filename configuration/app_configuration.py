from os import environ

from flask.app import Flask
from flask_restful import Api

db_uri_configuration = {
    'test': 'TEST_DATABASE_URI',
    'development': 'DEVELOPMENT_DATABASE_URI'
}


def get_configured_app(configuration_name: str):
    environ['SQLALCHEMY_DATABASE_URI'] = environ.get(db_uri_configuration[configuration_name])

    app = Flask(__name__)

    # TODO (fivkovic): Configure CSRF
    # TODO (fivkovic): Configure CORS

    restful_api = Api(app)

    from configuration.database_configuration import initialize_database
    initialize_database()

    # TODO (fivkovic): Add resources mapping to API

    return app

