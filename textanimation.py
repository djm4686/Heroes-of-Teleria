__author__ = 'Admin'
import pygame
class TextAnimation:
    def __init__(self, text, startpos, color = (255,0,0), duration = 125, fontsize = 20):
        self.text = text
        self.startx = startpos[0]
        self.starty = startpos[1]
        self.textColor = color
        self.curx = self.startx
        self.cury = self.starty
        self.duration = duration

        self.font = pygame.font.SysFont("monospace", fontsize)
        self.font.set_bold(True)
        self.label = self.font.render(self.text, 1, self.textColor)
        self.rect = self.label.get_rect()
        self.rect.center = startpos
        self.rect.y = self.rect.y - 75
    def animate(self, display):
        display.blit(self.label, self.rect)
        if self.rect.y < self.starty - self.duration:
            return False
        else:
            self.rect.y -= 1
            return True