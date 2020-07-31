from os import environ
from pyramid import testing

from invisibleroads_posts import configure_settings


def test_environment_constants(data_folder):
    config = testing.setUp(settings={
        'data.folder': data_folder,
        'application.environment': 'PIZZA=TIME\nCOWABUNGA = DUDE',
    })
    configure_settings(config)
    assert environ['PIZZA'] == 'TIME'
    assert environ['COWABUNGA'] == 'DUDE'


def test_secret_constants(data_folder):
    secret_length = 32
    config = testing.setUp(settings={
        'data.folder': data_folder,
        'secret.length': secret_length,
        'x.secret': '',
    })
    assert len(config.get_settings()['x.secret']) == 0
    configure_settings(config)
    assert len(config.get_settings()['x.secret']) == secret_length
