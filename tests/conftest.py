from pyramid.config import Configurator
from pyramid.response import Response


pytest_plugins = [
    'invisibleroads_posts.tests',
]


def get_app(global_config, **settings):

    def index(request):
        return Response('whee')

    with Configurator(settings=settings) as config:
        config.include('invisibleroads_posts')
        config.add_route('index', '/')
        config.add_view(index, route_name='index')
    return config.make_wsgi_app()
