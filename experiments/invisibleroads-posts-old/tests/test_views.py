from pyramid.httpexceptions import HTTPBadRequest
from pyramid.renderers import render
from pytest import raises

from invisibleroads_posts.tests import WEBSITE_VERSION
from invisibleroads_posts.views import expect_integer, expect_param


class TestExpectParam(object):

    def test_reject_missing_value(self, posts_request):
        posts_request.params = {}
        with raises(HTTPBadRequest):
            expect_param(posts_request, 'x')

    def test_reject_unexpected_value(self, posts_request):
        posts_request.params = {'x': 'x'}
        with raises(HTTPBadRequest):
            expect_param(posts_request, 'x', float)

    def test_accept_expected_value(self, posts_request):
        posts_request.params = {'x': 1.5}
        assert 1.5 == expect_param(posts_request, 'x', float)

    def test_accept_default(self, posts_request):
        posts_request.params = {}
        assert 1.5 == expect_param(posts_request, 'x', float, default='1.5')


class TestExpectInteger(object):

    def test_reject_small_value(self, posts_request):
        posts_request.params = {'x': '1'}
        with raises(HTTPBadRequest):
            expect_integer(posts_request, 'x', minimum=10)

    def test_reject_large_value(self, posts_request):
        posts_request.params = {'x': '100'}
        with raises(HTTPBadRequest):
            expect_integer(posts_request, 'x', maximum=10)

    def test_reject_non_integer(self, posts_request):
        posts_request.params = {}
        with raises(HTTPBadRequest):
            expect_integer(posts_request, 'x')

        posts_request.params = {'x': ''}
        with raises(HTTPBadRequest):
            expect_integer(posts_request, 'x')

        posts_request.params = {'x': 'x'}
        with raises(HTTPBadRequest):
            expect_integer(posts_request, 'x')

    def test_reject_unexpected_value(self, posts_request):
        posts_request.params = {'x': '1'}
        with raises(HTTPBadRequest):
            expect_integer(posts_request, 'x', expect_100)

    def test_accept_expected_value(self, posts_request):
        posts_request.params = {'x': '100'}
        assert 100 == expect_integer(posts_request, 'x', expect_100)

    def test_accept_default(self, posts_request):
        posts_request.params = {}
        assert 100 == expect_integer(posts_request, 'x', default='100')


def expect_100(x):
    if x != 100:
        raise ValueError
    return x
