from invisibleroads_macros_disk import remove_folder
from pyramid import testing
from pytest import fixture


@fixture
def posts_request(posts_config, data_folder):
    posts_request = testing.DummyRequest(data_folder=data_folder)
    posts_request.json_body = {}
    yield posts_request


@fixture
def posts_config(posts_settings):
    config = testing.setUp(settings=posts_settings)
    config.include('invisibleroads_posts')
    yield config
    testing.tearDown()


@fixture
def posts_settings(data_folder):
    yield {
        'data.folder': data_folder,
    }


@fixture
def data_folder(tmpdir):
    data_folder = str(tmpdir)
    yield data_folder
    remove_folder(data_folder)
