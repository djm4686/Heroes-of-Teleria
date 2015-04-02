import pygame

__author__ = 'Daniel Madden'




class RangedAttackAnimation:
    def __init__(self, hero1, hero2):
        self.sprite = pygame.image.load("images/arrow.png")
        self.startTile = hero1.getTile()
        self.endTile = hero2.getTile()
