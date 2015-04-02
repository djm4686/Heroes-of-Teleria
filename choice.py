__author__ = 'Admin'

import pygame

class Choice:

    def __init__(self, text, x, y, callback = None, params = []):
        self.text = text
        self.x = x
        self.y = y
        self.callback = callback
        self.params = params
        self.arrow = pygame.image.load("images/arrow_left.png")
        self.highlightColor = (99, 99, 99)
        self.highlight = False
        self.rect = pygame.Rect(x, y, 55, 15)
        self.arrowRect = pygame.Rect(0, 0, 10, 10)
        self.arrowRect.center = self.rect.center
        self.arrowRect.x += 45
        self.arrowRect.y -= 1

    def click(self):
        if self.callback != None:
            self.callback(*self.params)

    def mouseOver(self):
        self.highlight = True

    def collidepoint(self, point):
        return self.rect.collidepoint(point)

    def draw(self, surface):
        if self.highlight:
            surface.blit(self.arrow, self.arrowRect)
        surface.blit(self.text, self.rect)