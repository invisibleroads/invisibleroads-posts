from pyramid.paster import bootstrap, setup_logging


def load_bootstrapped_settings(configuration_path):
    'Use bootstrap to ensure same configuration as application'
    setup_logging(configuration_path)
    with bootstrap(configuration_path) as env:
        request = env['request']
        return request.registry.settings
