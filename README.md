Extra Notes
===========


Minitel used: Minitel 2, manufactured by Philips

To put the minitel in terminal mode, press `Fnct`-`T` followed by `V`.


# Setup

Install [Poetry](https://python-poetry.org/), then run `poetry install`.

Connect your minitel and test with

`python max-test.py`


# Developing

The `server` directory contains a minimal minitel display emulator that can be
controlled via an HTTP API.  It's meant to be used with a mock version of
PyMinitel in order to develop minitel apps in the browser, without the need for
an actual minitel. See the [README](./server/README.md).
