An http server that acts as a minimal minitel display emulator.

It's meant to be used with a mock version of PyMinitel in order to develop
minitel apps in the browser, without the need for an actual minitel. We could
have done this in curses but rendering the terminal as HTML will allow using the
minitel font and displaying double-size characters.

## Running the server:

You should install the [Minitel font](https://www.dafont.com/minitel.font) first, then as usual:

- `python -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `flask --app server run --debug`
