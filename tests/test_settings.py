from os import environ
from pyramid import testing

from invisibleroads_posts import configure_settings
from invisibleroads_posts.constants import SECRET_LENGTH


def test_environment_constants(data_folder):
    config = testing.setUp(settings={
        'data.folder': data_folder,
        'application.environment': 'PIZZA TIME\nCOWABUNGA DUDE',
    })
    configure_settings(config)
    assert environ['PIZZA'] == 'TIME'
    assert environ['COWABUNGA'] == 'DUDE'


def test_secret_constants(data_folder):
    config = testing.setUp(settings={
        'data.folder': data_folder,
        'x.secret': '',
    })
    configure_settings(config)
    settings = config.get_settings()
    assert len(settings['x.secret']) == SECRET_LENGTH
