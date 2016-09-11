InvisibleRoads Posts
====================
Posts form the foundation for most of our web applications.

- Pyramid_ 1.6.1
- Bootstrap_ 3.3.6
- JQuery_ 1.12.2


Use
---
Prepare environment. ::

    export VIRTUAL_ENV=~/.virtualenvs/crosscompute
    virtualenv ${VIRTUAL_ENV}
    source ${VIRTUAL_ENV}/bin/activate

    export NODE_PATH=${VIRTUAL_ENV}/lib/node_modules
    npm install -g uglify-js

Install package. ::

    PYTHON_PACKAGE=~/Projects/invisibleroads-packages/posts
    NODE_PACKAGE=${PYTHON_PACKAGE}/node_modules/invisibleroads-posts

    cd ~/Projects
    git clone git@github.com:invisibleroads/invisibleroads-posts.git

    cd ${PYTHON_PACKAGE}
    ${VIRTUAL_ENV}/bin/pip install -e .

Create project. ::

    cd ~/Projects
    ${VIRTUAL_ENV}/bin/pcreate -s ir-posts xyz

Install project. ::

    cd ~/Projects/xyz
    ${VIRTUAL_ENV}/bin/pip install -e .
    bash refresh.sh

Launch development server. ::

    ${VIRTUAL_ENV}/bin/pserve development.ini

Launch production server. ::

    ${VIRTUAL_ENV}/bin/pserve production.ini


Recreate
--------
Use starter scaffold. ::

    cd ~/Experiments
    ${VIRTUAL_ENV}/bin/pcreate -s starter invisibleroads-posts
    SOURCE_FOLDER=~/Projects/invisibleroads-posts
    TARGET_FOLDER=~/Experiments/invisibleroads-posts

Add .gitignore. ::

    wget https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore \
        -O ${TARGET_FOLDER}/.gitignore
    vimdiff ${TARGET_FOLDER}/.gitignore ${SOURCE_FOLDER}/.gitignore

Update configuration files. ::

    vimdiff ${TARGET_FOLDER}/MANIFEST.in ${SOURCE_FOLDER}/MANIFEST.in

    mv ${TARGET_FOLDER}/CHANGES.{txt,rst}
    vimdiff ${TARGET_FOLDER}/CHANGES.rst ${SOURCE_FOLDER}/CHANGES.rst

    mv ${TARGET_FOLDER}/README.{txt,rst}
    vimdiff ${TARGET_FOLDER}/README.rst ${SOURCE_FOLDER}/README.rst

    vimdiff ${TARGET_FOLDER}/development.ini ${SOURCE_FOLDER}/development.ini
    vimdiff ${TARGET_FOLDER}/production.ini ${SOURCE_FOLDER}/production.ini

    vimdiff ${TARGET_FOLDER}/setup.py ${SOURCE_FOLDER}/setup.py

Update package files. ::

    vimdiff \
        ${TARGET_FOLDER}/invisibleroads_posts/__init__.py \
        ${SOURCE_FOLDER}/invisibleroads_posts/__init__.py
    vimdiff \
        ${TARGET_FOLDER}/invisibleroads_posts/views.py \
        ${SOURCE_FOLDER}/invisibleroads_posts/views.py
    rm ${TARGET_FOLDER}/invisibleroads_posts/tests.py

Prepare templates. ::

    TEMPLATES_FOLDER=${TARGET_FOLDER}/invisibleroads_posts/templates
    rm ${TARGET_FOLDER}/invisibleroads_posts/templates/*
    mkdir ${TEMPLATES_FOLDER}
    cp ${SOURCE_FOLDER}/invisibleroads_posts/templates/* ${TEMPLATES_FOLDER}
    vim ${TEMPLATES_FOLDER}/base.jinja2
    vim ${TEMPLATES_FOLDER}/posts.jinja2

Prepare assets. ::

    ASSETS_FOLDER=${TARGET_FOLDER}/invisibleroads_posts/assets
    rm ${TARGET_FOLDER}/invisibleroads_posts/static/*
    mv ${TARGET_FOLDER}/invisibleroads_posts/static ${ASSETS_FOLDER}
    cp ${SOURCE_FOLDER}/invisibleroads_posts/assets/favicon.ico ${ASSETS_FOLDER}
    cp ${SOURCE_FOLDER}/invisibleroads_posts/assets/robots.txt ${ASSETS_FOLDER}
    cp ${SOURCE_FOLDER}/invisibleroads_posts/assets/whoops.html ${ASSETS_FOLDER}
    cd ${TARGET_FOLDER}
    bash refresh.sh

Add Bootstrap_. ::

    VERSION=3.3.6
    URL=https://github.com/twbs/bootstrap/releases/download
    cd ~/Documents
    wget ${URL}/v${VERSION}/bootstrap-${VERSION}-dist.zip
    unzip bootstrap-${VERSION}-dist.zip
    cd ~/Documents/bootstrap-${VERSION}-dist
    mkdir -p ${ASSETS_FOLDER}/bootstrap/css
    mkdir -p ${ASSETS_FOLDER}/bootstrap/js
    cp css/bootstrap.min.css ${ASSETS_FOLDER}/bootstrap/css
    cp js/bootstrap.min.js ${ASSETS_FOLDER}/bootstrap/js

Add JQuery_. ::

    VERSION=1.12.2
    cd ${ASSETS_FOLDER}
    wget http://code.jquery.com/jquery-${VERSION}.min.js -O jquery.min.js


.. _Pyramid: http://docs.pylonsproject.org/en/latest/docs/pyramid.html
.. _Bootstrap: http://getbootstrap.com
.. _JQuery: http://jquery.com
