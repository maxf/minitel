from flask import Flask, request

app = Flask(__name__)

NB_ROWS = 25
NB_COLS = 40

current_row = 0
current_col = 0

screen = []

def clear_screen():
    global screen
    screen = [[ "." for col in range(NB_COLS) ] for row in range(NB_ROWS)]

clear_screen()


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


@app.route("/", methods = ['GET'])
def hello_world():
    return minitel_as_html(screen)


@app.route("/envoyer", methods = ['POST'])
def envoyer():
    global current_col, current_row
    for char in request.form['contenu']:
        screen[current_row][current_col] = char
        if current_col < NB_COLS:
            current_col = current_col + 1
    return minitel_as_html(screen)


@app.route("/position", methods = ['POST'])
def position():
    global current_col, current_row
    if request.form['relatif'] == 'False':
        print('absolute')
        current_col = int(request.form['colonne'])
        current_row = int(request.form['ligne'])
    else:
        print('relatif')
        current_col += int(request.form['colonne'])
        current_row += int(request.form['ligne'])

    current_col = max(current_col, 0)
    current_col = min(current_col, NB_COLS-1)
    current_row = max(current_row, 0)
    current_row = min(current_row, NB_ROWS-1)
    print("=========", current_col, current_row)
    return minitel_as_html(screen)


@app.route("/efface", methods = ['POST'])
def efface():
    clear_screen()
    return minitel_as_html(screen)
