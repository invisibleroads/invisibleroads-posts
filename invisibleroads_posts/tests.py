from invisibleroads_macros.disk import remove_safely
from pyramid import testing
from pytest import fixture
from webtest import TestApp

from invisibleroads_posts import main as get_app


@fixture
def website(config, settings):
    config.include('pyramid_jinja2')
    yield TestApp(get_app({}, **settings))


@fixture
def config(settings):
    config = testing.setUp(settings=settings)
    yield config
    testing.tearDown()


@fixture
def settings(data_folder):
    return {
        'data.folder': data_folder,
    }


@fixture
def data_folder(tmpdir):
    data_folder = str(tmpdir)
    yield data_folder
    remove_safely(data_folder)
