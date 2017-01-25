InvisibleRoads Posts
====================
Posts form the foundation for most of our web applications.

Prepare environment. ::

    export VIRTUAL_ENV=~/.virtualenvs/crosscompute
    virtualenv ${VIRTUAL_ENV}
    source ${VIRTUAL_ENV}/bin/activate

Install package. ::

    PYTHON_PACKAGE=~/Projects/invisibleroads-packages/posts
    NODE_PACKAGE=${PYTHON_PACKAGE}/node_modules/invisibleroads-posts

    cd ~/Projects
    git clone git@github.com:invisibleroads/invisibleroads-posts

    cd ${PYTHON_PACKAGE}
    ${VIRTUAL_ENV}/bin/pip install -e .

Create project. ::

    cd ~/Projects
    ${VIRTUAL_ENV}/bin/pcreate -s ir-posts xyz

Install project. ::

    cd ~/Projects/xyz
    ${VIRTUAL_ENV}/bin/pip install -e .

Launch development server. ::

    ${VIRTUAL_ENV}/bin/pserve development.ini

Launch production server. ::

    ${VIRTUAL_ENV}/bin/pserve production.ini
