__author__ = 'Admin'
import pygame
from pygame.locals import *

class Stats:
    def __init__(self, pos, party1, party2, playerwin):
        self.x = pos[0]
        self.y = pos[1]
        self.party1 = party1
        self.party2 = party2
        self.playerwin = playerwin
        self.is_main = True
        self.getHeroRects()
        self.createUI()
    def createUI(self):
        self.mainRect = pygame.Rect(self.x, self.y, 500, 500)
        self.party1Rect = pygame.Rect(self.x + 10, self.y + 10, 245, 480)
        self.party2Rect = pygame.Rect(self.x + 255, self.y + 10, 245, 480)

    def getHeroRects(self):
        self.party1Rects = []
        self.party2Rects = []
        self.nameLabels = []
        self.currentHpLabels = []
        self.maxHpLabels = []
        self.xpLabels = []
        for x, i in zip(self.party1.getHeroes(), range(len(self.party1.getHeroes()))):
            self.nameLabels.append(x.getName())
            self.currentHpLabels.append(x.getCurrentHP())
            self.maxHpLabels.append(x.getMaxHp())
            self.party1Rects.append(pygame.Rect( self.x + 10, 10 + (i * 100), 245, 100))
        for x, i in zip(self.party2.getHeroes(), range(len(self.party2.getHeroes()))):
            self.nameLabels.append(x.getName())
            self.currentHpLabels.append(x.getCurrentHP())
            self.maxHpLabels.append(x.getMaxHp())
            self.party1Rects.append(pygame.Rect(self.x + 245 + 10, 10 + (i * 100), 245, 100))
    def eventLoop(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                self.is_main = False
    def draw(self, surface):
        s = pygame.Surface((600, 400))
        s.fill((255,255,255))
        surface.blit(s, self.mainRect)