#!/usr/bin/python

from PIL import Image
import os
import openai
import time
import curses
import sys
from curses import wrapper

from typing_extensions import Dict
from typing import TYPE_CHECKING, Dict, Any, List
if TYPE_CHECKING:
    from _curses import _CursesWindow
    Window = _CursesWindow
else:
    from typing import Any
    Window = Any


strings: Dict[str, str] = {
    "preprompt": "You are a kind assistant",
    "send": "Type your command, then press ",
    "next": "Next page:",
    "back": "To go back:",
    "intro": "Talk to ChatGPT",
    "intro2": "on your Minitel!",
    "tagline": "ChatGPT on your Minitel",
}


openai.api_key = os.getenv("OPENAI_API_KEY")


def ask_gpt(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": strings["preprompt"]},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    return response['choices'][0]['message']['content'].split('\n')


# im = Image.open("chatgpt-logo-pixellated-1-to-1.png")

NB_ROWS: int = 24
NB_COLS: int = 40
KEY_ENVOI: List[int] = [19, 65]
KEY_CORRECTION: List[int] = [19, 71]
KEY_RETOUR: List[int] = [19, 66]
KEY_SUITE: List[int] = [19, 72]


curses.setupterm(term="vt100")
#stdscr = curses.initscr()  # initialise curses
# curses.noecho()  # don't echo incoming characters



# minitel.efface()
# minitel.curseur(False)


# print(im.format, im.size, im.mode)
# print(im.getpixel((2,2)))


# def pixel(col: int, row: int):
#    return 0 if im.getpixel((col, row)) != (255, 255, 255) else 1


def button(stdscr: Window, row: int, col: int, text: str):
    stdscr.addstr(col, row, f" {text} ", curses.A_REVERSE)
    stdscr.refresh()


def wait_for(stdscr, keycode):
    input: str = ""
    while input != keycode:
        input = stdscr.getkey()


def require_input(stdscr: Window, row: int, col: int):
    # Input field

    stdscr.addstr(row, col, "........................................")
    stdscr.addstr(row+2, col, strings["send"])

    button(stdscr, col+len(strings["send"]), row+2, 'Envoi')

    input = ""
    input_pos = col
    while True:
        key: str = stdscr.getkey(row, input_pos)
        input_pos = input_pos + 1

        if key[0:4] == "KEY_":
            continue
        elif key == "\x7f":
            # backspace
            input_pos = input_pos - 2
            stdscr.addstr(row, input_pos, ".")
            input = input[:-1]
        elif key == "\n":
            # Return key
            break
        else:
            # displayable character
            stdscr.addstr(row, input_pos - 1, key)
            input = input + key

    return input


lookup = {
    "000000": " ",
    "111000": "'",
    "011110": ">",
    "001111": "\\",
    "111100": "/",
    "110000": "#",
    "100000": "!",
    "111010": "7",
    "000101": "H",
    "000111": "X",
    "000011": "P",
    "111101": "O",
    "001011": "T",
    "010000": "\"",
    "111111": "_",
    "000001": "@",
    "000010": "0",
    "110111": "[",
    "101111": "]",
    "011111": "^",
    "110100": "+",
    "111011": "W",
    "110101": "K",
    "001010": "4",
    "010100": "*",
    "101011": "U",
    "111110": "?",
}


# Build the logo

def show_logo():
    logo = []
    for row in range(0, 29, 3):
        line = ""
        for col in range(0, 30, 2):
            b = f"""{pixel(col, row)}{pixel(col+1, row)}{pixel(col, row+1)}
{pixel(col+1, row+1)}{pixel(col, row+2)}{pixel(col+1, row+2)}"""

            char = lookup.get(b, None)

            if char is None:
                print("missing", b)
                char = '.'

            line = line + char
        logo.append(line)


    # Draw the logo
    minitel.semigraphique()
    for row in range(4, 14):
        minitel.position(25, row-2)
        minitel.semigraphique()
        minitel.envoyer(logo[row-4])



def envoyer_lignes(lignes, col, row):
    minitel.position(col, row)
    for idx, ligne in enumerate(lignes):
        minitel.envoyer(ligne)
        minitel.position(0, 1, relatif=True)


#############################


def main(stdscr: Window):
    curses.cbreak()  # don't wait for Enter to handle keypresses

    stdscr.keypad(True)  # automatically decode special keys into constants

    stdscr.clear()
    stdscr.addstr(2, 1, "3615 GPT")

#    show_logo()

    stdscr.addstr(10, 1, strings["intro"])
    stdscr.addstr(12, 1, strings["intro2"])
    stdscr.refresh()

    while True:
        user_input = require_input(stdscr, 22, 1)
        stdscr.addstr(0, 0, f"(User typed: {user_input})                   ")

        if user_input == "quit":
            return


        # out: List[str] = ask_gpt(user_input)
        out: List[str] = ["Le Minitel (pour « Médium interactif par numérisation d'information téléphonique ») est un type de terminal informatique destiné à la connexion au service français de Vidéotex baptisé Télétel, commercialement exploité en France entre 1980 et 2012. Donnant accès à des services variés préfigurant ceux du futur Internet, et utilisant pour cela le réseau français Transpac qui lui-même préfigurait la future infrastructure de transmission d'Internet, il a hissé la France au premier plan de la télématique mondiale grâce au premier service au monde de fourniture gratuite ou payante d’informations télématiques. Il fut un succès considérable et resta longtemps en usage, y compris en concurrence d’Internet.", "Par métonymie, le mot « Minitel » a fini par désigner l'ensemble du service Vidéotex en France ainsi que les éléments de réseau (concentrateurs, points d'accès) destinés à rendre ce service. "]


        stdscr.clear()
        stdscr.addstr(0, 1, "3615 GPT")
        stdscr.addstr(2, 1, strings["tagline"])

        position_row = 6

        for ligne in out:
            stdscr.addstr(position_row, 1, ligne)
            position_row = position_row + len(ligne) // 40 + 1

            if position_row > 21:
                stdscr.addstr(23, 1, strings["next"])
                button(stdscr, 24, 3 + len(strings["next"]), 'Suite')
        #         minitel.curseur(False)
                wait_for(stdscr, "S")
                stdscr.clear()
                stdscr.addstr(1, 1, "3615 GPT")
                stdscr.addstr(3, 1, strings["tagline"])
                position_row = 6


        #     minitel.position(1, position_row)
        #     minitel.debut_ligne()

        #    minitel.envoyer(out)

#        minitel.position(2, 24)
#        minitel.envoyer(strings["back"])
#        button(3 + len(strings["back"]),24,'Retour')
#        minitel.curseur(False)
#        wait_for(KEY_RETOUR)

# minitel.efface()


wrapper(main)


# time.sleep(200)
