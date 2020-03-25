from invisibleroads_macros_disk import remove_folder
from pyramid import testing
from pytest import fixture


@fixture
def posts_request(application_config, data_folder):
    posts_request = testing.DummyRequest(data_folder=data_folder)
    posts_request.json_body = {}
    yield posts_request


@fixture
def application_config(config):
    config.include('invisibleroads_posts')
    yield config


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
    remove_folder(data_folder)
