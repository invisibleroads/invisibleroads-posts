from invisibleroads_macros_disk import remove_folder
from pyramid import testing
from pytest import fixture


@fixture
def posts_request(posts_config, data_folder):
    request = testing.DummyRequest(
        data_folder=data_folder)
    request.json_body = {}
    yield request


@fixture
def posts_config(posts_settings):
    config = testing.setUp(settings=posts_settings)
    config.include('invisibleroads_posts')
    yield config
    testing.tearDown()


@fixture
def posts_settings():
    return {
        'data.folder': data_folder,
        'secret.length': 32,
        'client_cache.http.expiration_time_in_seconds': 60,
    }


@fixture
def data_folder(tmpdir):
    data_folder = str(tmpdir)
    yield data_folder
    remove_folder(data_folder)
