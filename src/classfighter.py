from heroclass import *
import pygame, spriteextractor
from modifyercontainer import *
class ClassFighter(HeroClass):
    def __init__(self):
        HeroClass.__init__(self, "Fighter")
        self.skills = []
        self.mods = ModifyerContainer(2, 1.0, 3, .75, .5)
        self.hpMod = 10
        self.manaMod = 4
        s = spriteextractor.SpriteExtractor()
        self.sprites = s.extractSprites((32,36), "sprites/warrior_m.png")
        self.sprites2 = s.extractSprites((30,30), "images/Test_Unit_SS.png")
        self.sprites3 = []
        for x in range(len(self.sprites2)):
            self.sprites2[x] = pygame.transform.scale2x(self.sprites2[x])
            self.sprites3.append(pygame.transform.flip(self.sprites2[x], 1, 0))

        self.image = pygame.transform.scale(pygame.image.load("images/Class_creation_warrior.png"), (300,600))
        self.sprite = pygame.image.load("images/fighter.png")
    def getD1Sprites(self):
        return self.sprites[9::]
    def getD2Sprites(self):
        return self.sprites3[0::]
    def getD3Sprites(self):
        return self.sprites2[0::]
    def getD4Sprites(self):
        return self.sprites[3:6]
    def getD5Sprites(self):
        return self.sprites2[0::]
    def getD6Sprites(self):
        return self.sprites[9::]
    def getManaMod(self):
        return self.manaMod
    def getHpMod(self):
        return self.hpMod
    def getSkills(self):
        return self.skill
    def getModifyers(self):
        return self.mods
    def getArmorMod(self):
        return self.armorMod
    def getSprites(self):
        return self.sprites
    def getSprite(self):
        return self.sprites[7]
