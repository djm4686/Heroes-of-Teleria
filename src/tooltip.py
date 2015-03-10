__author__ = 'Admin'
import pygame

class ToolTip:

    def __init__(self, name, text, pos, size = (200, 100)):
        self.name = name
        self.text = text
        self.pos = pos
        self.size = size
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.textLabels = []
        self.createLabels()

    def createBox(self):
        self.mainRect = pygame.Rect(self.pos, self.size)
        self.backgroundRect = pygame.Rect(self.pos[0] + 5, self.pos[1] + 5, self.size[0] - 10, self.size[1] - 10)
        self.descriptionRect = pygame.Rect(self.pos[0] + 5, self.pos[1] + 25, self.size[0] - 10, self.size[1] -10)

    def createLabels(self):
        self.nameLabel = self.font.render(self.name, True, (255,255,255))

        if len(self.text) > 30:
            i = 0
            texts = []
            lastCrimp = 0
            for x, y in zip(self.text, range(len(self.text))):
                if x == " " and y > 25 * (i + 1):
                    texts.append(self.text[lastCrimp:y])
                    lastCrimp = y + 1
                    i = i + 1
            texts.append(self.text[lastCrimp::])
            for x in texts:
                self.textLabels.append(self.font.render(x, True, (255,255,255)))
        else:
            self.textLabels = [self.font.render(self.text, True, (255,255,255))]
    def draw(self, surface, point):
        self.pos = point
        if self.pos[1] + 100 > 600:
            self.pos = point[0], point[1] - 100
        self.createBox()
        print self.textLabels
        pygame.draw.rect(surface, (255,255,255), self.mainRect)
        pygame.draw.rect(surface, (0,0,0), self.backgroundRect)
        surface.blit(self.nameLabel, self.backgroundRect)
        for x in self.textLabels:
            surface.blit(x, self.descriptionRect)
            self.descriptionRect.y += 14