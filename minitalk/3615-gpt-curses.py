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

    return response['choices'][0]['message']['content']


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
    stdscr.addstr(row, col, f" {text} ", curses.A_REVERSE)
    stdscr.refresh()


def wait_for(stdscr: Window, keycode: str) -> None:
    input: str = ""
    while input != keycode:
        input = stdscr.getkey()


def require_input(stdscr: Window, row: int, col: int):
    # Input field

    stdscr.addstr(row, col, "........................................")
    stdscr.addstr(row+2, col, strings["send"])

    button(stdscr, row+2, col+len(strings["send"]), 'Envoi')

    input = ""
    input_pos = col
    while True:
        key: str = stdscr.getkey(row, input_pos)

        if key[0:4] == "KEY_":
            continue
        elif key == "\x7f":
            # backspace
            input_pos = input_pos - 1
            stdscr.addstr(row, input_pos, ".")
            input = input[:-1]
        elif key == "\n":
            # Return key
            break
        else:
            # displayable character
            input_pos = input_pos + 1
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

    stdscr.addstr(0, 0, f"rows: {curses.LINES}, cols: {curses.COLS}")


    stdscr.addstr(2, 1, "3615 GPT")

#    show_logo()

    stdscr.addstr(10, 1, strings["intro"])
    stdscr.addstr(12, 1, strings["intro2"])
    stdscr.refresh()

    while True:
        user_input = require_input(stdscr, curses.LINES - 3, 0)
        stdscr.addstr(0, 0, f"(User typed: {user_input})                   ")

        if user_input == "quit":
            return


        response: str = ask_gpt(user_input)


        # prepare the result for display
        # 1. replace \n by however much whitespace needed to reach the end
        # of the line
        while (i := response.find('\n')) != -1:
            nb_padding_spaces = curses.COLS - i % curses.COLS
            response = response.replace("\n", " " * nb_padding_spaces, 1)


        # paginate the output
        nb_chars_per_page = curses.COLS * (curses.LINES - 8)
        pages =  [ response[i:i + nb_chars_per_page] for i in range(0, len(response), nb_chars_per_page) ]


        stdscr.clear()
        stdscr.addstr(1, 1, "3615 GPT")
        stdscr.addstr(2, 1, strings["tagline"])


        for page in pages:
            stdscr.addstr(6, 0, page)

            stdscr.addstr(curses.LINES - 1, 0, strings["next"])
            button(stdscr, curses.LINES - 1, 3 + len(strings["next"]), 'Suite')
            wait_for(stdscr, "S")
            stdscr.clear()
            stdscr.addstr(0, 1, "3615 GPT")
            stdscr.addstr(2, 1, strings["tagline"])


wrapper(main)
