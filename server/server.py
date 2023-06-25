from flask import Flask, request
from flask_sock import Sock
import time

app = Flask(__name__)
sock = Sock(app)

NB_ROWS = 25
NB_COLS = 40

current_row = 0
current_col = 0

char_width = 1
char_height = 1

screen = []

app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}

@sock.route('/ws')
def websocket(ws):
    while True:
        # data = ws.receive()
        # print(f"ws received {data}")
        time.sleep(3)
        ws.send(screen_as_html(screen))
    # ws.close(102, "that's all")

def clear_screen():
    global screen
    screen = [[ " " for col in range(NB_COLS) ] for row in range(NB_ROWS)]

clear_screen()


def screen_as_html(screen):
    result = ""
    for row in range(NB_ROWS):
        for col in range(NB_COLS):
            char = screen[row][col]
            if char != "":
                result = result + f"<text x={(col+1)*13} y={(row+1)*16}>{char}</text>"
    return f"""
      <svg width=1000 height=1000>
        <g transform="translate(5, 8)">
          <rect
            x=6 y=-5
            width={(NB_COLS+1)*13} height={(NB_ROWS+1)*16}
            stroke=#000 stroke-width=2px fill=#555></rect>
          {result}
        </g>
      </svg>
    """


def minitel_as_html(screen):
    return f"""<!DOCTYPE html>
    <html>
      <head>
        <link rel=stylesheet href="static/main.css" type="text/css">
      </head>
      <body>
        <p id=message>-</p>
        <div id=screen>{screen_as_html(screen)}</div>
        <script src="/static/main.js"></script>
        <script src="/static/node_modules/eruda/eruda.js"></script>
        <script>eruda.init();</script>
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
        current_col = int(request.form['colonne'])
        current_row = int(request.form['ligne'])
    else:
        current_col += int(request.form['colonne'])
        current_row += int(request.form['ligne'])

    current_col = max(current_col, 0)
    current_col = min(current_col, NB_COLS-1)
    current_row = max(current_row, 0)
    current_row = min(current_row, NB_ROWS-1)
    return minitel_as_html(screen)


@app.route("/efface", methods = ['POST'])
def efface():
    clear_screen()
    return minitel_as_html(screen)

@app.route("/taille", methods = ['POST'])
def taille():
    char_width = request.form['largeur']
    char_height = request.form['hauteur']
