from os import environ

from configuration.app_configuration import get_configured_app

if __name__ == '__main__':
    app = get_configured_app(configuration_name='development')
    app.run(host=environ.get('FLASK_RUN_HOST'))
