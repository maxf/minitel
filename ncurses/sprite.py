import curses

class Sprite:
    def __init__(self, y, x, id, content):
        self.y = y
        self.x = x
        self.id = id
        self.content = content
        self.background = []

    def save_background(self, win):
        self.background = [win.inch(self.y, self.x + i) for i in range(len(self.content))]

    def restore_background(self, win):
        for i, char in enumerate(self.background):
            win.addch(self.y, self.x + i, char)

    def draw(self, win):
        self.save_background(win)
        win.addstr(self.y, self.x, self.content, curses.A_REVERSE)

    def delete(self, win):
        self.restore_background(win)

    def move_to(self, win, y, x):
        self.delete(win)
        self.y = y
        self.x = x
        self.draw(win)
