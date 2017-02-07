from pyramid.httpexceptions import HTTPBadRequest
from pyramid.renderers import render
from pytest import raises

from invisibleroads_posts.views import expect_integer, expect_param


class TestAddRoutes(object):

    def test_index(self, website):
        website.get('')
        website.get('/site.min.css')
        website.get('/site.min.js')

    def test_bad_request(self, config, website):
        route_name = 'x.json'
        route_url = '/x.json'

        def see_x_json(request):
            raise HTTPBadRequest({})

        config.add_route(route_name, route_url)
        config.add_view(see_x_json, route_name=route_name)
        website.get(route_url, status=404)

    def test_page_not_found(self, website):
        response = website.get('/x', status=404)
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
        with raises(HTTPBadRequest):
            expect_integer('x', {'x': '1'}, lambda x: x == 10)

    def test_reject_small_value(self):
        with raises(HTTPBadRequest):
            expect_integer('x', {'x': '1'}, minimum_value=10)

    def test_reject_large_value(self):
        with raises(HTTPBadRequest):
            expect_integer('x', {'x': '100'}, maximum_value=10)

    def test_accept_expected_value(self):
        assert 100 == expect_integer('x', {'x': '100'})


class TestExpectParam(object):

    def test_reject_missing_value(self):
        with raises(HTTPBadRequest):
            expect_param('x', {})

    def test_reject_reject_unexpected_value(self):
        with raises(HTTPBadRequest):
            expect_param('x', {'x': 'x'}, float)

    def test_accept_expected_value(self):
        assert 'x' == expect_param('x', {'x': 'x'})
