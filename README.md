# Information to load and test this project

This project is just a Proof of Concept before deploying it as part of a larger Django project
(hence the text files instead of a database)

## Installing the project

- Clone the repo
- cd into the top level of the project
- create a venv:
> python3 -m venv venv
- install the requirements
> pip3 install -r requirements
- signup and get your binance api key and secret
- load them into your ~/.bashrc file
> export api_key="enter your key here"
> export api_secret="enter your secret here"
- run project by:
> python3 start.py

## Running the tests

- from the top level:
> python3 -m unittest discover

## To run the coverage:

- from the top level:
> coverage run -m unittest discover
> coverage report --omit="venv/*,*/__init__*"
- to show lines that are missing coverage
> coverage report -m --omit="venv/*,*/__init__*"
