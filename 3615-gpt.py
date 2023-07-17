#from minitel import Minitel
from emunitel import Minitel
from PIL import Image

import time
im = Image.open("chatgpt-logo-pixellated-1-to-1.png")

NB_ROWS = 24
NB_COLS = 40

minitel = Minitel.Minitel()
vitesse = minitel.deviner_vitesse()
print("vitesse", vitesse)

if (vitesse == -1):
    result = minitel.definir_vitesse(4802)
    print('result', result)

minitel.identifier()
minitel.efface()

minitel.position(2, 3)
minitel.taille(2,2)
minitel.envoyer("3615 GPT")

print(im.format, im.size, im.mode)
#print(im.getpixel((2,2)))

def pixel(col, row):
    return 0 if im.getpixel((col, row)) != (255, 255, 255) else 1




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


lines = []

for row in range(0,29,3):
    line = ""
    for col in range(0,30,2):
        b = f"{pixel(col, row)}{pixel(col+1, row)}{pixel(col, row+1)}{pixel(col+1, row+1)}{pixel(col, row+2)}{pixel(col+1, row+2)}"

        char = lookup.get(b, None)

        if char == None:
            print("missing", b)
            char = '.'

        line = line + char
    lines.append(line)



minitel.semigraphique()

for row in range(4, 14):
    minitel.position(25, row-2)
    minitel.semigraphique()
    minitel.envoyer(lines[row-4])

time.sleep(200)
minitel.close()
