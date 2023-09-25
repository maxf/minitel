from PIL import Image
import os
import openai
import time
import curses
import sys
from curses import wrapper


# Init openai

LANG = 'en'

strings = {
    "fr": {
        "preprompt": "Tu es un gentil assistant",
        "send": "Tapez votre commande, puis ",
        "next": "Page suivante:",
        "back": "Revenir au début:",
        "intro": "Interrogez ChatGPT",
        "intro2": "sur votre Minitel!",
        "tagline": "ChatGPT sur votre Minitel",
    },
    "en": {
        "preprompt": "You are a kind assistant",
        "send": "Type your command, then press ",
        "next": "Next page:",
        "back": "To go back:",
        "intro": "Talk to ChatGPT",
        "intro2": "on your Minitel!",
        "tagline": "ChatGPT on your Minitel",
    }
}


openai.organization = "org-SXynwmSaKFYwkwqBBnzAZO5m"
openai.api_key = os.getenv("OPENAI_API_KEY")


def ask_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": strings[LANG]["preprompt"]},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    return response['choices'][0]['message']['content'].split('\n')


im = Image.open("chatgpt-logo-pixellated-1-to-1.png")

NB_ROWS = 24
NB_COLS = 40
KEY_ENVOI = [19, 65]
KEY_CORRECTION = [19, 71]
KEY_RETOUR = [19, 66]
KEY_SUITE = [19, 72]

stdscr = curses.initscr()  # initialise curses
# curses.noecho()  # don't echo incoming characters
curses.cbreak()  # don't wait for Enter to handle keypresses
stdscr.keypad(True)  # automatically decode special keys into constants




# minitel.efface()
# minitel.curseur(False)


print(im.format, im.size, im.mode)
# print(im.getpixel((2,2)))


def pixel(col, row):
    return 0 if im.getpixel((col, row)) != (255, 255, 255) else 1


def button(row, col, text):
    stdscr.addstr(col, row, f" {text} ", curses.A_REVERSE)
    stdscr.refresh()


def wait_for(keycode):
    input = Sequence()
    while True:
        input = minitel.recevoir_sequence(True, None)
        if input.valeurs == keycode:
            return


def require_input(row, col):
    # Input field

    stdscr.addstr(row, col, "........................................")
    stdscr.addstr(row+2, col, strings[LANG]["send"])

    button(col+len(strings[LANG]["send"]), row+2, 'Envoi')

    input = ""
    input_pos = col
    while True:
        c = stdscr.getch(row, input_pos)
        input_pos = input_pos + 1

        if c == 263:  # backspace key
            input_pos = input_pos - 2
            stdscr.addstr(row, input_pos, ".")
            input = input[:-1]
        elif c == 10:  # Return key
            break
        else:
            input = input + chr(c)

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


def main():
    stdscr.clear()

    stdscr.addstr(2, 1, "3615 GPT")

#    show_logo()

    stdscr.addstr(10, 1, strings[LANG]["intro"])
    stdscr.addstr(12, 1, strings[LANG]["intro2"])
    stdscr.refresh()

    while True:
        user_input = require_input(22, 1)
        stdscr.addstr(0, 0, f"(User typed: {user_input})                   ")

        if user_input == "quit":
            sys.exit()


        #        out = ask_gpt(user_input)

        #stdscr.clear()
        #        stdscr.addstr(1, 0, "3615 GPT")

        # minitel.position(1, 2)
        # minitel.taille(2, 2)
        # minitel.envoyer("3615 GPT")
        # minitel.position(1, 3)
        # minitel.envoyer(strings[LANG]["tagline"])

        # position_row = 6

        # minitel.position(1, position_row)
        # for ligne in out:
        #     minitel.envoyer(ligne)
        #     position_row = position_row + len(ligne) // 40 + 1

        #     if position_row > 21:
        #         minitel.position(2, 24)
        #         minitel.envoyer(strings[LANG]["next"])
        #         button(3 + len(strings[LANG]["next"]), 24, 'Suite')
        #         minitel.curseur(False)
        #         wait_for(KEY_SUITE)
        #         minitel.efface()
        #         minitel.position(1, 2)
        #         minitel.taille(2, 2)
        #         minitel.envoyer("3615 GPT")
        #         minitel.position(1, 3)
        #         minitel.envoyer(strings[LANG]["tagline"])
        #         position_row = 6


        #     minitel.position(1, position_row)
        #     minitel.debut_ligne()

        #    minitel.envoyer(out)

#        minitel.position(2, 24)
#        minitel.envoyer(strings[LANG]["back"])
#        button(3 + len(strings[LANG]["back"]),24,'Retour')
#        minitel.curseur(False)
#        wait_for(KEY_RETOUR)

# minitel.efface()


wrapper(main())


# time.sleep(200)
