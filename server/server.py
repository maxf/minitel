from flask import Flask

app = Flask(__name__)

NB_ROWS = 25
NB_COLS = 40

screen = [[ "X" for col in range(NB_COLS) ] for row in range(NB_ROWS)]


def char_as_html(char):
    return f"<td>{char}</td>"

def row_as_html(row):
    return "<tr>" + ''.join([char_as_html(char) for char in row]) + "</tr>"

def screen_as_html(screen):
    return "<table>" + ''.join([row_as_html(row) for row in screen]) + "</table>"


def minitel_as_html(screen):
    return f"""<!DOCTYPE html>
    <html>
      <head>
        <link rel=stylesheet href="static/main.css" type="text/css">
      </head>
      <body>
        {screen_as_html(screen)}
      </body>
    </html>
    """


@app.route("/")
def hello_world():
    return minitel_as_html(screen)
