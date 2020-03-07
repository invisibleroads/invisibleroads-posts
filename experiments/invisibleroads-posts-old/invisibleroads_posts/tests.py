from invisibleroads_macros.disk import remove_safely
from pyramid import testing
from pytest import fixture
from webtest import TestApp

from invisibleroads_posts import main as get_app


@fixture
def posts_website(posts_request):
    settings = posts_request.registry.settings
    yield TestApp(get_app({}, **settings))


@fixture
def posts_request(website_config, data_folder):
    posts_request = testing.DummyRequest(
        data_folder=data_folder, scheme='http')
    posts_request.__dict__['registry'] = posts_request.registry
    yield posts_request


@fixture
def website_config(config):
    config.include('invisibleroads_posts')
    yield config


@fixture
def config(settings):
    config = testing.setUp(settings=settings)
    yield config
    testing.tearDown()


@fixture
def data_folder(tmpdir):
