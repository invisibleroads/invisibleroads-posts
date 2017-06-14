from pyramid.httpexceptions import HTTPBadRequest
from pyramid.renderers import render
from pytest import raises

from invisibleroads_posts.views import expect_integer, expect_param


class TestAddRoutes(object):

    def test_index(self, posts_website):
        posts_website.get('')
        posts_website.get('/site.min.css')
        posts_website.get('/site.min.js')

    def test_page_not_found(self, posts_website):
        response = posts_website.get('/x', status=404)
        assert response.text == render(
            'invisibleroads_posts:templates/404.jinja2', {})


class TestExpectInteger(object):

    def test_reject_non_integer(self):
        with raises(HTTPBadRequest):
            expect_integer('x', {})
        with raises(HTTPBadRequest):
            expect_integer('x', {'x': ''})
        with raises(HTTPBadRequest):
            expect_integer('x', {'x': 'x'})

    def test_reject_unexpected_value(self):

        def parse(x):
            if x != 10:
                raise ValueError
            return x

        with raises(HTTPBadRequest):
            expect_integer('x', {'x': '1'}, parse)

    def test_reject_small_value(self):
        with raises(HTTPBadRequest):
            expect_integer('x', {'x': '1'}, minimum=10)

    def test_reject_large_value(self):
        with raises(HTTPBadRequest):
            expect_integer('x', {'x': '100'}, maximum=10)

    def test_accept_expected_value(self):
        assert 100 == expect_integer('x', {'x': '100'})

    def test_accept_default(self):
        assert 100 == expect_integer('x', {}, default='100')


class TestExpectParam(object):

    def test_reject_missing_value(self):
        with raises(HTTPBadRequest):
            expect_param('x', {})

    def test_reject_unexpected_value(self):
        with raises(HTTPBadRequest):
            expect_param('x', {'x': 'x'}, float)

    def test_accept_expected_value(self):
        assert 1.5 == expect_param('x', {'x': 1.5}, float)

    def test_accept_default(self):
        assert 1.5 == expect_param('x', {}, float, default='1.5')
