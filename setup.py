from os.path import abspath, dirname, join
from setuptools import find_packages, setup


ENTRY_POINTS = '''
[invisibleroads]
initialize = invisibleroads_posts.scripts:InitializePostsScript
'''
APPLICATION_CLASSIFIERS = [
    'Programming Language :: Python',
    'Framework :: Pyramid',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    'License :: OSI Approved :: MIT License',
]
APPLICATION_REQUIREMENTS = [
    # web
    'pyramid',
    # cache
    'dogpile.cache',
    # shortcut
    'invisibleroads >= 0.2.4',
    'invisibleroads-macros-configuration >= 1.0.5',
    'invisibleroads-macros-descriptor >= 1.0.1',
    'invisibleroads-macros-disk >= 1.0.2',
    'invisibleroads-macros-security >= 1.0.0',
    'invisibleroads-macros-text >= 1.0.1',
]
TEST_REQUIREMENTS = [
    'pytest-cov',
    'webtest',
]
FOLDER = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(FOLDER, x)).read().strip() for x in [
    'README.md', 'CHANGES.md'])


setup(
    name='invisibleroads-posts',
    version='0.7.10',
    description='Web application defaults',
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    classifiers=APPLICATION_CLASSIFIERS,
    author='Roy Hyunjin Han',
    author_email='rhh@crosscompute.com',
    url='https://github.com/invisibleroads/invisibleroads-posts',
    keywords='web wsgi bfg pylons pyramid invisibleroads',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    extras_require={'test': TEST_REQUIREMENTS},
    install_requires=APPLICATION_REQUIREMENTS,
    entry_points=ENTRY_POINTS)
