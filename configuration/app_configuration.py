from flask.app import Flask
from flask_restful import Api


def get_configured_app(configuration_name: str):
    app = Flask(__name__)

    # TODO (fivkovic): Configure CSRF
    # TODO (fivkovic): Configure CORS

    restful_api = Api(app)

    # TODO (fivkovic): Initialize DB
    # TODO (fivkovic): Add resources mapping to API

    return app
