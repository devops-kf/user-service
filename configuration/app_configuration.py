from os import environ

from flask.app import Flask
<<<<<<< Updated upstream
from flask_restful import Api
from flask_wtf import CSRFProtect

db_uri_configuration = {
    'test': 'TEST_DATABASE_URI',
    'development': 'DEVELOPMENT_DATABASE_URI'
}
=======
from flask_jwt_extended import JWTManager

jwt_manager = JWTManager()


class Configuration:
    DEBUG = False
    TESTING = False
    JSON_SORT_KEYS = False

    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')

    JWT_TOKEN_LOCATION = "headers"
    JWT_HEADER_NAME = "Authorization"       # Same as default
    JWT_HEADER_TYPE = "Bearer"              # Same as default
    JWT_ALGORITHM = "RS256"
    JWT_DECODE_ALGORITHMS = ["RS256"]
    JWT_PUBLIC_KEY = open('configuration/public_key.pem', encoding='utf-8').read()  # Asymmetric RS256 algorithm is used
    JWT_DECODE_AUDIENCE = "access"
    JWT_DECODE_ISSUER = "authentication-api"
    JWT_ERROR_MESSAGE_KEY = "message"


class DevelopmentConfiguration(Configuration):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEVELOPMENT_DATABASE_URI')


class TestingConfiguration(Configuration):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('TEST_DATABASE_URI')


class ProductionConfiguration(Configuration):
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
>>>>>>> Stashed changes


def get_configured_app(configuration_name: str):
    environ['SQLALCHEMY_DATABASE_URI'] = environ.get(db_uri_configuration[configuration_name])

<<<<<<< Updated upstream
    app = Flask(__name__)
=======
    set_app_configuration(app, configuration_name)
    configure_csrf(app)
    configure_cors(app)

    from configuration.database_configuration import initialize_database
    initialize_database(app.config.get('SQLALCHEMY_DATABASE_URI'))

    jwt_manager.init_app(app)

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
>>>>>>> Stashed changes

    if environ.get('ENABLE_CSRF') == 1:
        app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
        app.config['WTF_CSRF_SECRET_KEY'] = environ.get('WTF_CSRF_SECRET_KEY')
        csrf = CSRFProtect()
        csrf.init_app(app)

    # TODO (fivkovic): Configure CORS

    restful_api = Api(app)

    from configuration.database_configuration import initialize_database
    initialize_database()

    # TODO (fivkovic): Add resources mapping to API

<<<<<<< Updated upstream
    return app

=======
    from controller.user_accounts_controller import UsersResource
    from controller.follow_requests_controller import FollowRequestsResource, AcceptFollowRequestResource,\
        RejectFollowRequestResource
    from controller.user_profiles_controller import UserProfilesResource, FollowRelationshipsResource,\
        BlockRelationshipsResource, MuteUserProfileResource, UnMuteUserProfileResource

    def create_resource_uri(value):
        return f'/v1{value}'

    # TODO (fivkovic): On users endpoint return on get all followers/following/muted/blocked for current user ???

    restful_api.add_resource(UsersResource,
                             create_resource_uri('/users'))
    restful_api.add_resource(FollowRequestsResource,
                             create_resource_uri('/follow-requests'))
    restful_api.add_resource(AcceptFollowRequestResource,
                             create_resource_uri('/follow-requests/<request_id>/accept'))
    restful_api.add_resource(RejectFollowRequestResource,
                             create_resource_uri('/follow-requests/<request_id>/reject'))
    restful_api.add_resource(UserProfilesResource,
                             create_resource_uri('/user-profiles/<target_user_profile_id>'))
    restful_api.add_resource(FollowRelationshipsResource,
                             create_resource_uri('/user-profiles/<target_user_profile_id>/follow'))
    restful_api.add_resource(BlockRelationshipsResource,
                             create_resource_uri('/user-profiles/<target_user_profile_id>/block'))
    restful_api.add_resource(MuteUserProfileResource,
                             create_resource_uri('/user-profiles/<target_user_profile_id>/mute'))
    restful_api.add_resource(UnMuteUserProfileResource,
                             create_resource_uri('/user-profiles/<target_user_profile_id>/un-mute'))
>>>>>>> Stashed changes
