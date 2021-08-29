from configuration.app_configuration import get_configured_app


if __name__ == '__main__':
    get_configured_app(configuration_name='development').run()          # TODO (fivkovic): Define host for app
