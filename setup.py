from os.path import abspath, dirname, join
from setuptools import find_packages, setup


ENTRY_POINTS = """
[paste.app_factory]
main = invisibleroads_posts:main
[pyramid.scaffold]
ir-posts = invisibleroads_posts.scaffolds:PostsTemplate
ir-python = invisibleroads_posts.scaffolds:PythonTemplate
[invisibleroads]
initialize = invisibleroads_posts.scripts:InitializePostsScript
"""
FOLDER = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(FOLDER, x)).read().strip() for x in [
    'README.rst', 'CHANGES.rst'])
setup(
    name='invisibleroads-posts',
    version='0.5.1',
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
    keywords='web wsgi bfg pylons pyramid invisibleroads',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    setup_requires=[
        'pytest-runner',
    ],
    install_requires=[
        'pyramid>=1.6.0',
        'pyramid_debugtoolbar',
        'waitress',
    ] + [
        'dogpile.cache',
        'invisibleroads>=0.1.6',
        'invisibleroads_macros>=0.7.1',
        'pyramid_jinja2',
        'simplejson',
        'titlecase',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'webtest',
    ],
    entry_points=ENTRY_POINTS)
