__author__ = 'Admin'
import pygame
class Stats:
    def __init__(self, pos, party1, party2, playerwin):
        self.x = pos[0]
        self.y = pos[1]
        self.party1 = party1
        self.party2 = party2
        self.playerwin = playerwin
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
            self.maxHpLabels.append(x.getMaxHP())
            self.party1Rects.append(pygame.Rect( self.x + 10, 10 + (i * 100), 245, 100))
        for x, i in zip(self.party1.getHeroes(), range(len(self.party2.getHeroes()))):
            self.nameLabels.append(x.getName())
            self.currentHpLabels.append(x.getCurrentHP())
            self.maxHpLabels.append(x.getMaxHP())
            self.party1Rects.append(pygame.Rect(self.x + 245 + 10, 10 + (i * 100), 245, 100))

    def draw(self, surface):
        pass