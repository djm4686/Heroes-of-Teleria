import pygame
class Button:
    def __init__(self, textLabel = None, callBack = None, cbparams = [], rect = pygame.Rect(0,0,100,50), color = (152,172,186), textColor = (0,0,0)):
        self.textLabel = textLabel
        self.textRect = self.textLabel.get_rect()
        self.rect = rect
        self.color = color
        self.textColor = textColor
        self.cb = callBack
        self.textRect.center = self.rect.center
        self.cbparams = cbparams
    def setText(self, textLabel):
        self.textLabel = textLabel
        self.textRect = self.textLabel.get_rect()
        self.textRect.center = self.rect.center
    def getText(self):
        pass
    def setCenter(self, point):
        self.rect.center = point
        self.textRect.center = point
    def setRect(self, rect):
        self.rect = rect
        self.textRect.center = self.rect.center
    def collidepoint(self, p):
        return self.rect.collidepoint(p)
    def getRect(self):
        return self.rect
    def setCallback(self, callback):
        self.cb = callback
    def getCallback(self):
        return self.cb
    def callBack(self):
        if len(self.cbparams)>0:
            self.cb(self.cbparams)
        else:
            self.cb()
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, self.textColor, self.rect, 1)
        surface.blit(self.textLabel, self.textRect)
