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
    version='0.5.5.1',
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
    url='https://github.com/invisibleroads/invisibleroads-posts',
    keywords='web wsgi bfg pylons pyramid invisibleroads',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    setup_requires=[
        'pytest-runner',
    ],
    install_requires=[
        'pyramid-debugtoolbar',
        'pyramid>=1.7.3',
        'waitress',
    ] + [
        'dogpile.cache',
        'invisibleroads-macros>=0.8.3',
        'invisibleroads>=0.2.0',
        'paste',
        'pyramid-jinja2',
        'pytest',
        'simplejson',
        'titlecase',
        'webtest',
    ],
    tests_require=[
        'pytest-cov',
    ],
    entry_points=ENTRY_POINTS)
