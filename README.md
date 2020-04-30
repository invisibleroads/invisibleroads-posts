# InvisibleRoads Posts

Posts form the foundation for our web applications.

## Use

Install dependencies.

    pip install -U cookiecutter

Initialize project.

    cookiecutter https://github.com/invisibleroads/invisibleroads-cookiecutter

Follow the instructions in the generated README.

## Test

    git clone https://github.com/invisibleroads/invisibleroads-posts
    cd invisibleroads-posts
    pip install -e .[test]
    pytest --cov=invisibleroads_posts --cov-report term-missing tests
