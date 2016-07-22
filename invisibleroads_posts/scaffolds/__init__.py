from pyramid.scaffolds import PyramidTemplate


class PostsTemplate(PyramidTemplate):

    _template_dir = 'posts'
    summary = 'InvisibleRoads Posts'


class PythonTemplate(PyramidTemplate):

    _template_dir = 'python'
    summary = 'InvisibleRoads Package in Python'
