# Project Structure
We will follow the MVC structure as it is in the unit outline
flask application have different ways to structure a project
here are some helpful links
- https://teaching.csse.uwa.edu.au/units/CITS3403/lectures/10MVC.pdf
- https://stackoverflow.com/q/14415500
- https://flask-diamond.readthedocs.io/en/latest/model-view-controller/
- https://gist.github.com/cuibonobo/8696392
- https://exploreflask.com/en/latest/organizing.html#organization-patterns
- https://github.com/datahappy1/flask_mvc_github_example_project
- https://flask.palletsprojects.com/en/2.0.x/patterns/packages/

## Small Notes
routers/controllers folders are similar
views/templates folders are similar


# How to run
## install poetry
for better dependency management poetry will be used.
follow the [official installation guide](https://python-poetry.org/docs/master/#installing-with-the-official-installer)
for the steps.

## prepare the environment
To install and configure all needed packages simply run
```shell
poetry install
```
and to get into a poetry shell with all needed tools run
```shell
poetry shell
```

## run the server
there is a pre-configured script called `flask-app`. just run it in the command line
```shell
flask-app
```
and you will have your server up.


## run the test
simply run the following in the root directory of the project
```shell
pytest
```