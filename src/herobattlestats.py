import pygame
class HeroBattleStats:
    def __init__(self, hero):
        self.hero = hero
        self.bgImage = pygame.transform.scale2x(pygame.image.load("images/panel_blue.png"))
    def makeText(self, text):
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
        return self.font.render(text, True, (0,0,0))
    def makeLabels(self):
        self.nameLabel = self.makeText(self.hero.getName())
        self.levelLabel = self.makeText("Lvl: " + str(self.hero.getLevel()))
        self.hpLabel = self.makeText("HP: " + str(self.hero.getCurrentHp()) + "/" + str(self.hero.getMaxHp()))
        self.manaLabel = self.makeText("Mana: " + str(self.hero.getCurrentMana()) + "/" + str(self.hero.getMaxMana()))
        self.meleeWeaponLabel = self.makeText("Melee: " + self.hero.getMeleeWeapon().getName())
        self.rangedWeaponLabel = self.makeText("Ranged: " + self.hero.getRangedWeapon().getName())
        self.armorLabel = self.makeText("Armor: " + self.hero.getArmor().getName())
        self.shieldLabel = self.makeText("Shield: " + self.hero.getShield().getName())
        
    def draw(self, surface):
        self.makeLabels()
        surface.blit(self.bgImage, pygame.Rect(0,400,200,200))
        surface.blit(self.nameLabel, pygame.Rect(10, 410, 100, 20))
        surface.blit(self.hpLabel, pygame.Rect(10, 425, 100, 20))
        surface.blit(self.manaLabel, pygame.Rect(10, 440, 100, 20))
        surface.blit(self.meleeWeaponLabel, pygame.Rect(10, 455, 100, 20))
        surface.blit(self.rangedWeaponLabel, pygame.Rect(10, 470, 100, 20))
        surface.blit(self.armorLabel, pygame.Rect(10, 485, 100, 20))
        surface.blit(self.shieldLabel, pygame.Rect(10, 500, 100, 20))
        surface.blit(self.levelLabel, pygame.Rect(110, 410, 100, 20))
        
