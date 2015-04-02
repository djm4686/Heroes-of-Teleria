__author__ = 'Admin'

class ArrowAnimation:
    def __init__(self, startpos, endpos):
        self.startx = startpos[0]
        self.starty = startpos[1]
        self.endx = endpos[0]
        self.endy = endpos[1]
        self.curx = self.startx
        self.cury = self.starty

        self.rect = self.label.get_rect()
        self.rect.center = startpos
        self.rect.y = self.rect.y - 75
        if self.endy > self.starty:
            self.heightMaxX = abs(self.starty - self.endy)/2 + self.starty
        if self.endy < self.starty:
            self.heightMaxX = abs(self.starty - self.endy)/2 + self.endy

    def update(self):
        pass

    def draw(self):
        pass