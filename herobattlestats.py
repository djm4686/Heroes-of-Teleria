import pygame
import hpbar

class HeroBattleStats:
    def __init__(self, hero, x, y):
        self.hero = hero
        self.x = x
        self.y = y
        self.bgImage = pygame.image.load("images/herostatbg.png")
        self.i = 0
    def makeText(self, text):
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
        return self.font.render(text, True, (0,0,0))
    def makeLabels(self):
        self.nameLabel = self.makeText(self.hero.getName())
        self.levelLabel = self.makeText("Lvl: " + str(self.hero.getLevel()))
        self.hpLabel = self.makeText("HP: " + str(self.hero.getCurrentHp()) + "/" + str(self.hero.getMaxHp()))
        self.manaLabel = self.makeText("MP: " + str(self.hero.getCurrentMana()) + "/" + str(self.hero.getMaxMana()))
        self.meleeWeaponLabel = self.makeText("Melee: " + self.hero.getMeleeWeapon().getName())
        self.rangedWeaponLabel = self.makeText("Ranged: " + self.hero.getRangedWeapon().getName())
        self.armorLabel = self.makeText("Armor: " + self.hero.getArmor().getName())
        self.shieldLabel = self.makeText("Shield: " + self.hero.getShield().getName())
        self.sprites = self.hero.getActiveHeroClass().getD2Sprites()
        self.hpbar = hpbar.HPBar(self.hero.maxhp, self.hero.currentHp, self.x + 10, self.y + 40, 75)
        self.manabar = hpbar.HPBar(self.hero.maxMana, self.hero.currentMana, self.x + 10, self.y + 70, 75)

    def draw(self, surface, i = 0):
        self.makeLabels()
        self.hpbar.update(self.hero.currentHp)
        self.manabar.update(self.hero.currentMana)
        surface.blit(self.bgImage, pygame.Rect(self.x,self.y,200,200))
        surface.blit(self.nameLabel, pygame.Rect(self.x + 10, self.y + 10, 100, 20))
        surface.blit(self.hpLabel, pygame.Rect(self.x + 10,  self.y + 25, 100, 20))
        self.hpbar.draw(surface)
        self.manabar.draw(surface, color = (0, 0, 255))
        surface.blit(self.manaLabel, pygame.Rect(self.x + 10, self.y + 55, 100, 20))
        #surface.blit(self.meleeWeaponLabel, pygame.Rect(10, 555, 100, 20))
        #surface.blit(self.rangedWeaponLabel, pygame.Rect(10, 570, 100, 20))
        #surface.blit(self.armorLabel, pygame.Rect(10, 585, 100, 20))
        #surface.blit(self.shieldLabel, pygame.Rect(10, 600, 100, 20))
        surface.blit(self.levelLabel, pygame.Rect(self.x + 110, self.y + 10, 100, 20))
        surface.blit(self.sprites[i], pygame.Rect(self.x + 95, self.y + 25, 60, 60))
        
