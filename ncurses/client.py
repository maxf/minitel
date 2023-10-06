#!/usr/bin/python
import socket
import threading
import curses
import random
import string
import json
import os
import locale
from sprite import Sprite


from typing import TYPE_CHECKING, Dict, Any, List
if TYPE_CHECKING:
    from _curses import _CursesWindow
    Window = _CursesWindow
else:
    Window = Any

ROWS, COLS = 24, 40

sprites: List[Sprite] = []

def random_id(length: int=10):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def draw(message: Dict[str, Any], screen: Window):
    if message["type"] == "sync":
        # Draw the entire canvas on the terminal
        # TODO: rewrite so only the non-whitespace is drawn, otherwise it's
        # going to be very slow on old terminals
        screen.clear()
        for row, canvas_line in enumerate(message["canvas"]):
            screen.addstr(row, 0, canvas_line)
    elif message["type"] == "update":
        row = message["row"]
        col = message["col"]
        # only update the canvas with the single character received
        if message["client_id"] != client_id:
            # This is a message from another client, so display
            # a tag with their ID

            # first look if there's already a tag with that id
            s = list(filter(lambda t: t.id == message['client_id'], sprites))
            if len(s) == 1:
                s[0].move_to(screen, row, col + 1)
            else:
                new_tag = Sprite(row, col + 1, message['client_id'], message['username'])
                new_tag.draw(screen)
                sprites.append(new_tag)
        screen.addstr(row, col, message["text"])

    else:
        raise Exception(f"Unknown message type: {message['type']}")
    screen.move(cursor_row, cursor_col)
    screen.refresh()



cursor_row: int = 0
cursor_col: int = 0
client_id: str = random_id()
username: str = ""

def receive_data(s, screen: Window):
    """
    Handle data that has been sent from the server
    """
    while True:
        data: str = s.recv(1048576).decode() # 512x512x4 - kinda random

        # data should be a JSON string as:
        # { "type": "update", "text": "...", "row": ..., "col": ..., "client_id": ..., "username": "..." }
        # or
        # { "type": "sync", "canvas": "..." }
        if not data:
            curses.endwin()
            print("Connection closed by the server.")
            break

        data_as_obj: Dict[str, Any] = json.loads(data)

        draw(data_as_obj, screen)


def main(screen) -> None:
    curses.cbreak()  # Enable char-by-char input mode
    curses.noecho()  # Don't echo characters back to the screen
    screen.keypad(1)  # Handle special keystrokes

    HOST, PORT = "127.0.0.1", 9999
    global cursor_row, cursor_col

    screen.addstr(f"Connecting to {HOST}:{PORT}...\n")
    screen.refresh()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Start a thread to listen for incoming data
        threading.Thread(target=receive_data, args=(s, screen)).start()

        try:
            # counter = 1
            while True:
                ch: int = screen.getch()
                # screen.addstr(counter, 1, f"{counter}/1: user typed {ch}")
                # screen.refresh()
                # counter = counter + 1

                if ch == 27:  # Escape character. E.g. minitel special keys
                    # Try to get the next characters with a timeout
                    screen.nodelay(1)  # Non-blocking mode
                    next_ch = screen.getch()

                    if next_ch == ord('['):
                        final_ch = screen.getch()
                        if final_ch == 66: # key down
                            cursor_row = min(ROWS-1, cursor_row + 1)
                        elif final_ch == 65: # key up
                            cursor_row = max(0, cursor_row - 1)
                        elif final_ch == 68: # key left
                            cursor_col = max(0, cursor_col - 1)
                        elif final_ch == 67: # key right
                            cursor_col = min(COLS-1, cursor_col + 1)
                        else:
                            continue
                    screen.nodelay(0)  # Back to blocking mode
                elif ch in [127, 263] and cursor_col > 0: # backspace
                    cursor_col = cursor_col - 1
                    update = {
                        "type": "update",
                        "text": ".",
                        "row": cursor_row,
                        "col": cursor_col,
                        "client_id": client_id,
                        "username": username
                    }
                    draw(update, screen)
                    s.sendall(json.dumps(update).encode())
                elif ch == 258: # key down
                    cursor_row = min(ROWS-1, cursor_row + 1)
                elif ch == 259: # key up
                    cursor_row = max(0, cursor_row - 1)
                elif ch == 260: # key left
                    cursor_col = max(0, cursor_col - 1)
                elif ch == 261: # key right
                    cursor_col = min(COLS-1, cursor_col + 1)
                else:
                    # normal character
                    update = {
                        "type": "update",
                        "text": chr(ch),
                        "row": cursor_row,
                        "col": cursor_col,
                        "client_id": client_id,
                        "username": username
                    }
                    cursor_col = min(COLS-1, cursor_col + 1)
                    # draw on this terminal
                    draw(update, screen)
                    # send the update to the server
                    s.sendall(json.dumps(update).encode())
                screen.move(cursor_row, cursor_col)

        finally:
            s.close()
            screen.addstr("\nConnection closed. Press any key to exit.\n")
            screen.refresh()
            screen.getch()  # Wait for another key press before exiting


if __name__ == "__main__":

    print("Connected to the minitalk server")
    print(f"terminal type: {os.getenv('TERM')}")

    # ask for the user name
    while len(username) == 0:
        username = input("What's your user name? ")

        username = "<" + username # small arrow for the tag


    # start the canvas editor
    curses.wrapper(main)
