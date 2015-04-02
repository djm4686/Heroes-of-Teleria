__author__ = 'Admin'
import pygame

class HPBar:

    def __init__(self, maxhp, currenthp, x, y, max = 46.0):
        self.hp = currenthp
        self.maxHP = maxhp
        self.x = x
        self.y = y
        self.backgroundImage = pygame.image.load("images/hpbar.png")
        self.rect = pygame.Rect(x, y, max + 4, 10)
        self.maxSize = max
        self.backgroundImage = pygame.transform.smoothscale(self.backgroundImage, (int(self.maxSize + 4), 10))
        self.hpRect = pygame.Rect(self.x + 2, self.y + 2, self.maxSize, 6)
        self.hpRect.width = (float(self.hp)/float(self.maxHP)) * self.maxSize

    def update(self, currentHP):
        self.hp = currentHP
        self.hpRect.width = (float(self.hp)/float(self.maxHP)) * self.maxSize

    def setCenter(self, point):
        self.rect.center = point
        self.hpRect.center = point

    def setPoint(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.hpRect.x = x + 2
        self.hpRect.y = y + 2

    def draw(self, surface, color = (255, 0, 0)):
        surface.blit(self.backgroundImage, self.rect)
        pygame.draw.rect(surface, color, self.hpRect)
