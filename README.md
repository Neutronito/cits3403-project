# Play our game on the [CITS3403.com](https://cits3403.com) domain!

# Project Structure
We will follow the MVC structure, as it is in the unit outline.
Here are some helpful links on how this structure is done.
- https://teaching.csse.uwa.edu.au/units/CITS3403/lectures/10MVC.pdf
- https://stackoverflow.com/q/14415500
- https://flask-diamond.readthedocs.io/en/latest/model-view-controller/
- https://gist.github.com/cuibonobo/8696392
- https://exploreflask.com/en/latest/organizing.html#organization-patterns
- https://github.com/datahappy1/flask_mvc_github_example_project
- https://flask.palletsprojects.com/en/2.0.x/patterns/packages/

## Small Notes
Route and controller folders are similar to one another.
View and template folders are also similar to one another.

# Purpose of Our Web Application
The purpose of our web application is to provide a way for people to practice and hone their HTML and CSS front end skills and knowledge through a fun and interesting game.

This game aims to simulate real website development by giving the user a criteria, or end goal/design, and then rating there score on how well they achieved this design. The aim of the game is to obtain the highest score by matching the design exactly, which is how a real-word situation would be, where a client/company requires a certains site to be made according to their criteria and requirements.

# Architecture of Our Web Application
## How It Works
Our web application works by storing "HTML maps". This is simply a big string stored in the database which contains all the HTML for the required criteria. Any CSS must be included in the same document. 

When the user wishes to play the map of a certain day, the map for that day is found and its HTML is sent to a chromium browser. A screenshot is then taken of the site rendered, and sent to the user as an image. The user is then given a box to write the HTML in, which should render to match the image given.

The user can preview their HTML, which will send the string to the backend where a screenshot is taken (in the same way as the map screenshot) and then sent back to the user. 

Once the user is ready to submit, a screenshot is taken of the HTML. However, this time, the image is compared to the screenshot of the initial map, using an image comparison algorithm. This returns a score from 0 - 100, where 0 is no match at all, and 100 is an exact replica of the map. This score is then displayed to the user and stored in the database. The goal is to match the map exactly, and so recieve a score of 100.

## File Structure
Each section has been given its own directory, which contains the statics, views, controllers and models (if it has any). There are currently 5 sections:

### Admin
This is where all the administration aspects occur. This serves the admin page to the user if they are an admin.
This page shows information on all the users, and contains the api calls to modify users and their information.
It also shows a list of all the maps, and contains the api calls to delete and add maps.

### Auth
This is the authentication section, and deals with the creation of users and logging in.
It serves the HTML to login or signup (depending on the user request), and deals with the flask aspect of these things.
It contains the WTForms that are filled in for logging in and signing up.
It also contains the table which stores all the details of the users.

## Game
This is where all the game aspects are dealt with.
It serves the HTML to play the game.
It contains the majority of the api calls required, such as getting the map, previewing HTML, modifying a users count and retrieving their count
It also contains two tables which store the counts of all the users, and also all the maps.

## Home
This is the simplest directory, all it does is serve the homepage which contains some information about the game.

## Leaderboard
This deals with the leaderboard and displaying it.
It serves the HTML which allows the user to see the different scores. 
It also contains some api calls to obtain information from the database and allow the creation of the leaderboard.


# How to run everything

## On Our Domain
The easiest way to play our game is on our domain, which can be found at [CITS3403.com](https://cits3403.com). This requires no setup, all you need to do is create an account and you can play the game.
However, there is a chance there will be no map for the day, as we are not actively maintaining the site and adding maps in. You may add in your own maps through the admin account, which has a username admin and password admin.

## Using Python Virtual Environment
```shell
git clone https://gitlab.com/qdog/cits3403-project.git
cd cits3403-project
python3.9 -m venv cits3403-venv
source cits3403-venv/bin/activate
pip install .  # you can add the -e option if you want to edit the code

flask-db upgrade
flask-create-admin -u admin -p admin
flask-production --bind 127.0.0.1:5000 --log-level=DEBUG
```

## Using Docker
If you want to just test things out without any persistent data
```shell
docker run --rm -p 5000:5000 -it registry.gitlab.com/qdog/cits3403-project:master --bind 0.0.0.0:5000 --log-level=debug 
```
To store the database outside of Docker, use the environment variable SQLALCHEMY_DATABASE_URI. You can see more environment 
variables to edit within the [settings.py](src/flask_app/settings.py) file
```shell
mkdir db
docker run --rm -p 5000:5000 -v ./db:/db
  -e SQLALCHEMY_DATABASE_URI=sqlite:////db/sqlite.db
  -dt registry.gitlab.com/qdog/cits3403-project:master --bind 0.0.0.0:5000 --log-level=debug 
```

## Using Poetry
For better dependency management, we have used Poetry.
Follow the [official installation guide](https://python-poetry.org/docs/master/#installing-with-the-official-installer)
for the installation steps.
```shell
git clone https://gitlab.com/qdog/cits3403-project.git
cd cits3403-project
poetry shell
poetry install

flask-db upgrade
flask-create-admin -u admin -p admin
flask-production --bind 127.0.0.1:5000 --log-level=DEBUG
```

# How to Run the Tests
we are using Selenium and Chrome has been tested to work correctly.
Make sure you have either Chrome or Chromium installed and Chromium-driver installed
## On Bare Metal
You will need Poetry here since there are required app dependencies and development dependencies
```shell
poetry install --dev
pytest
```

## Using Docker
First we need to build the Docker image with the argument `DEV` given.
```shell
docker build --build-arg DEV=y -t cits3403-project 
```
Now we can run it
```shell
docker run --rm --entrypoint pytest -it cits3403-project 
```


# Gitflow
The workflow is like the following
1 - create an issue
2 - create a merge request
3 - squash the branch commits
4 - merge with master


# FAQ
## Where Is the requirements.txt File?
We used poetry, which uses [pyproject.toml](pyproject.toml) and [poetry.lock](poetry.lock) to get the correct dependencies.
If you wish to obtain the proper requirements.txt, you can produce this with
```shell
poetry export -f requirements.txt
```

## Why Docker?
Since the app requires Chromium to render HTML and not all of us (developers) have or want to install Chromium, Docker ensured
everyone has the same environment.
