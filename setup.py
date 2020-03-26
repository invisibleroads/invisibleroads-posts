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
    # test
    'pytest',
    # cache
    'dogpile.cache',
    # shortcut
    'invisibleroads',
    'invisibleroads-macros-configuration',
    'invisibleroads-macros-descriptor',
    'invisibleroads-macros-disk',
    'invisibleroads-macros-security',
    'invisibleroads-macros-text',
]
TEST_REQUIREMENTS = [
    'pytest-cov',
]
FOLDER = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(FOLDER, x)).read().strip() for x in [
    'README.md', 'CHANGES.md'])


setup(
    name='invisibleroads-posts',
    version='0.7.1',
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
    zip_safe=False,
    extras_require={'test': TEST_REQUIREMENTS},
    install_requires=APPLICATION_REQUIREMENTS,
    entry_points=ENTRY_POINTS)
