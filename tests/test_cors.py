import webtest
from pytest import fixture

from conftest import get_app


@fixture
def cors_application(posts_request):
    settings = posts_request.registry.settings
    settings['cors.allowed_origins'] = 'example.com test.com'
    settings['cors.allowed_methods'] = 'GET POST'
    settings['cors.allowed_headers'] = 'Authorization'
    yield webtest.TestApp(get_app({}, **settings))


def test_cors_preflight(cors_application):
    response = cors_application.options('/')
    assert 'Access-Control-Allow-Origin' not in response.headers

    response = cors_application.options('/', headers={
        'Origin': 'abc.com',
        'Access-Control-Request-Method': 'GET',
    })
    headers = response.headers
    assert 'Access-Control-Allow-Origin' not in headers
    assert 'Access-Control-Allow-Methods' not in headers
    assert 'Access-Control-Allow-Headers' not in headers

    response = cors_application.options('/', headers={
        'Origin': 'example.com',
        'Access-Control-Request-Method': 'GET',
    })
    headers = response.headers
    assert headers['Access-Control-Allow-Origin'] == 'example.com'
    assert headers['Access-Control-Allow-Methods'] == 'GET,POST'
    assert headers['Access-Control-Allow-Headers'] == 'Authorization'


def test_cors(cors_application):
    response = cors_application.options('/', headers={
        'Origin': 'abc.com',
    })
    assert 'Access-Control-Allow-Origin' not in response.headers

    response = cors_application.options('/', headers={
        'Origin': 'example.com',
    })
    headers = response.headers
    assert headers['Access-Control-Allow-Origin'] == 'example.com'
    assert headers['Vary'] == 'Origin'
