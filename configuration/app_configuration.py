from os import environ

from flask.app import Flask


class Configuration:
    DEBUG = False
    TESTING = False
    JSON_SORT_KEYS = False

    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')


class DevelopmentConfiguration(Configuration):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEVELOPMENT_DATABASE_URI')


class TestingConfiguration(Configuration):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('TEST_DATABASE_URI')


class ProductionConfiguration(Configuration):
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')


def get_configured_app(configuration_name: str):
    app = Flask(__name__)

    set_app_configuration(app, configuration_name)
    configure_csrf(app)
    configure_cors(app)

    from configuration.database_configuration import initialize_database
    initialize_database(app.config.get('SQLALCHEMY_DATABASE_URI'))

    initialize_error_handlers(app)
    register_resources(app)

    return app


def set_app_configuration(app, configuration_name: str):
    if configuration_name == 'development':
        app.config.from_object('configuration.app_configuration.DevelopmentConfiguration')
    elif configuration_name == 'test':
        app.config.from_object('configuration.app_configuration.TestingConfiguration')
    else:
        app.config.from_object('configuration.app_configuration.ProductionConfiguration')


def configure_csrf(app):
    from flask_wtf import CSRFProtect

    if environ.get('ENABLE_CSRF') == 1:
        app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
        app.config['WTF_CSRF_SECRET_KEY'] = environ.get('WTF_CSRF_SECRET_KEY')
        csrf = CSRFProtect()
        csrf.init_app(app)


def configure_cors(app):
    # TODO (fivkovic): Configure CORS
    pass


def initialize_error_handlers(app):
    from exception.api_error import ApiError

    @app.errorhandler(ApiError)
    def exception_handler(e):
        return e.to_response()


def register_resources(app):
    from flask_restful import Api

    restful_api = Api(app)

    from controller.user_accounts_controller import UsersResource

    restful_api.add_resource(UsersResource, '/users')
