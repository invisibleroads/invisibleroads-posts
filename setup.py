from os.path import abspath, dirname, join
from setuptools import find_packages, setup


ENTRY_POINTS = """
[paste.app_factory]
main = invisibleroads_posts:main
[pyramid.scaffold]
posts = invisibleroads_posts.scaffolds:PostsTemplate
[invisibleroads]
initialize = invisibleroads_posts.scripts:InitializePostsScript
"""
REQUIREMENTS = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
] + [
    'dogpile.cache',
    'invisibleroads',
    'invisibleroads_macros',
    'pyramid_jinja2',
    'titlecase',
]
FOLDER = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(FOLDER, x)).read().strip() for x in [
    'README.rst', 'CHANGES.rst'])
setup(
    name='invisibleroads-posts',
    version='0.4.1',
    description='Web application defaults',
    long_description=DESCRIPTION,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    author='Roy Hyunjin Han',
    author_email='rhh@crosscompute.com',
    url='http://invisibleroads.com',
    keywords='web pyramid pylons invisibleroads',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    entry_points=ENTRY_POINTS)
