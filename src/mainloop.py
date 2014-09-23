import pygame as pg
import hexboard
from pygame.locals import *
class MainLoop:
    def __init__(self):
        pg.init()
        self.surface = pg.display.set_mode((800,600))
        self.board = hexboard.HexBoard(10,10)
        self.main()
    def main(self):
        while True:
            self.surface.fill((255,255,255))
            self.board.drawTiles(self.surface)
            pg.display.update()
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
if __name__ == "__main__":
    m = MainLoop()
