from flask import Flask

app = Flask(__name__)


screen = [[ "X" for col in range(80) ] for row in range(72)]


def char_as_html(char):
    return f"<td>{char}</td>"

def row_as_html(row):
    return "<tr>" + ''.join([char_as_html(char) for char in row]) + "</tr>"

def screen_as_html(screen):
    return "<table>" + ''.join([row_as_html(row) for row in screen]) + "</table>"

@app.route("/")
def hello_world():
    return screen_as_html(screen)
