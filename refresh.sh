#!/bin/bash
MODULE_NAMES="invisibleroads_posts"
for MODULE_NAME in ${MODULE_NAMES}; do
    PARENT_FOLDER=`python -c "import ${MODULE_NAME}; from os.path import abspath, dirname; print(dirname(dirname(abspath(${MODULE_NAME}.__file__))))"`
    NODE_FOLDER=${PARENT_FOLDER}/node_modules/${MODULE_NAME/_/-}
    PYTHON_FOLDER=${PARENT_FOLDER}/${MODULE_NAME}
    pushd ${NODE_FOLDER} > /dev/null; npm install -g; popd > /dev/null
    if [[ "$1" == "--debug" || "$1" == "-d" ]]; then
        JS=`browserify ${NODE_FOLDER}/base.js`
    else
        JS=`browserify ${NODE_FOLDER}/base.js | uglifyjs -c`
    fi
    echo "$JS" > ${PYTHON_FOLDER}/assets/base.js
done
