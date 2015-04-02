__author__ = 'Admin'
import pygame
import choice

class ChoiceBox:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("images/choicebg.png")
        self.rect = pygame.Rect(x, y, 75, 100)
        self.choiceSurface = pygame.Surface((55, 80))

        self.choices = []

    def addChoice(self, text, cb, tooltip, tooltiptext, params=[]):
        x = self.x + 10
        y = self.y + (len(self.choices) * 20) + 10
        c = choice.Choice(text, x, y, cb, params)
        self.choices.append(c)

    def clearHighlights(self):
        for x in self.choices:
            x.highlight = False

    def clearChoices(self):
        self.choices = []

    def collidepoint(self, point):
        for x in self.choices:
            if x.collidepoint(point):
                return x

    def draw(self, surface):
        if len(self.choices) > 0:
            surface.blit(self.image, self.rect)
            for x in self.choices:
                x.draw(surface)

