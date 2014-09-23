from heroclass import *
from modifyercontainer import *
import pygame, spriteextractor
class ClassHealer(HeroClass):
    def __init__(self):
        HeroClass.__init__(self, "Healer")
        self.skills = []
        self.mods = ModifyerContainer(.5, .5, .75, 2, 4)
        self.hpMod = 6
        self.manaMod = 10
        s = spriteextractor.SpriteExtractor()
        self.sprites = s.extractSprites((32,36), "sprites/healer_m.png")
        self.sprite = pygame.image.load("images/healer.png")
    def getD1Sprites(self):
        return self.sprites[9::]
    def getD2Sprites(self):
        return self.sprites[0:3]
    def getD3Sprites(self):
        return self.sprites[3:6]
    def getD4Sprites(self):
        return self.sprites[3:6]
    def getD5Sprites(self):
        return self.sprites[6:9]
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

