Extra Notes
===========


Minitel used: Minitel 2, manufactured by Philips

To put the minitel in terminal mode, press `Fnct`-`T` followed by `V`.


# Setup

## With poetry

- `poetry install`
- `poetry run flask --app server run --debug`

## With pip

For environments that don't support poetry, like Termux on Android


- `python -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`

# Running

Connect your minitel and test with

- `poetry run max-test.py`


# Developing

The `server` directory contains a minimal minitel display emulator that can be
controlled via an HTTP API.  It's meant to be used with a mock version of
PyMinitel in order to develop minitel apps in the browser, without the need for
an actual minitel. We could have done this in curses but rendering the terminal
as HTML will allow using the minitel font and displaying double-size characters.

## Running the server:

### With poetry

- `poetry install`
- `poetry run flask --app server run --debug`

### With pip

For environments that don't support poetry, like Termux on Android

- `python -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements-frozen.txt`
- `flask --app server run --debug`

