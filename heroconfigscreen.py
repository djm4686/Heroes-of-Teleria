import pygame, imagebutton, leftarrowbutton, rightarrowbutton, button, multilinetextbutton
from globalvars import *
from pygame.locals import *
class HeroConfigScreen:
    def __init__(self, hero, surface):
        self.hero = hero
        self.surface = surface
        self.initVars()
        self.mainLoop()
    def initVars(self):
        self.weaponButtons = []
        self.backgroundColor = (128,128,128)
        self.ismain = True
        self.nameFont = pygame.font.Font(pygame.font.get_default_font(), 40)
        self.textFont = pygame.font.Font(pygame.font.get_default_font(), 18)
        self.nameLabel = self.nameFont.render(self.hero.getName() + " -", True, (0,0,0))
        self.hpLabel = self.makeText("HP:" + str(self.hero.getMaxHp()))
        self.raceLabel = self.makeText(self.hero.getRace().getName())
        self.activeClassLabel = self.makeText(self.hero.getActiveHeroClass().getName())
        self.levelLabel = self.nameFont.render("Level " + str(self.hero.getLevel()), True, (0,0,0))
        self.quitButton = imagebutton.ImageButton(pygame.image.load("images/back_button.png"), self.previousSurface)
        self.quitButton.setRect(pygame.Rect(self.surface.get_rect().width - 100, 0, 100, 50))
        self.professionLabel = pygame.font.Font(pygame.font.get_default_font(), 34).render("Profession:", True, (0,0,0))
        self.heroClassLabel = pygame.font.Font(pygame.font.get_default_font(), 34).render(self.hero.getActiveHeroClass().getName(), True, (0,0,0))
        self.leftClassButton = leftarrowbutton.LeftArrowButton(self.changeClassLeft)
        self.rightClassButton = rightarrowbutton.RightArrowButton(self.changeClassRight)
        self.strLabel = self.makeText("Strength: " + str(self.hero.getStr()))
        self.agiLabel = self.makeText("Agility: " + str(self.hero.getAgi()))
        self.conLabel = self.makeText("Constitution: " + str(self.hero.getCon()))
        self.intLabel = self.makeText("Intelligence: " + str(self.hero.getInt()))
        self.wisLabel = self.makeText("Wisdom: " + str(self.hero.getWis()))
        self.meleeButton = multilinetextbutton.MultiLineTextButton([self.makeText("Melee"), self.makeText("Equipped: " + self.hero.getMeleeWeapon().getName())], self.makeMeleeUI, rect = pygame.Rect(600, 50, 200, 100))
        self.rangedButton = multilinetextbutton.MultiLineTextButton([self.makeText("Ranged"), self.makeText("Equipped: " + self.hero.getRangedWeapon().getName())], self.makeRangedUI, rect = pygame.Rect(600, 150, 200, 100))
        self.armorButton = multilinetextbutton.MultiLineTextButton([self.makeText("Armor"), self.makeText("Equipped: " + self.hero.getArmor().getName())], self.makeArmorUI, rect = pygame.Rect(600, 250, 200, 100))
        self.shieldButton = multilinetextbutton.MultiLineTextButton([self.makeText("Shield"), self.makeText("Equipped: " + self.hero.getShield().getName())], self.makeShieldUI, rect = pygame.Rect(600, 350, 200, 100))
    def makeMeleeUI(self):
        if len(self.weaponButtons) == 0:
            for w in MELEE_WEAPONS:
                    self.weaponButtons.append(button.Button(pygame.font.Font(pygame.font.get_default_font(), 12).render(w.getName(), True, (0,0,0)), self.assignMeleeWeapon, [w], tooltipName="Spell: {}".format(w.getSpell().getName()), tooltipText=w.getSpell().getDescription()))
        else:
            self.weaponButtons = []
    def makeRangedUI(self):
        if len(self.weaponButtons) == 0:
            for w in RANGED_WEAPONS:
                    self.weaponButtons.append(button.Button(pygame.font.Font(pygame.font.get_default_font(), 12).render(w.getName(), True, (0,0,0)), self.assignRangedWeapon, [w]))
        else:
            self.weaponButtons = []
    def makeArmorUI(self):
        if len(self.weaponButtons) == 0:
            for w in ARMOR:
                    self.weaponButtons.append(button.Button(pygame.font.Font(pygame.font.get_default_font(), 12).render(w.getName(), True, (0,0,0)), self.assignArmor, [w], ))
        else:
            self.weaponButtons = []
    def makeShieldUI(self):
        if len(self.weaponButtons) == 0:
            for w in SHIELDS:
                    self.weaponButtons.append(button.Button(pygame.font.Font(pygame.font.get_default_font(), 12).render(w.getName(), True, (0,0,0)), self.assignShield, [w]))
        else:
            self.weaponButtons = []
    def changeClassLeft(self):
        i = CLASSES.index(self.hero.getActiveHeroClass())
        if i == 0:
            self.hero.activeHeroClass = CLASSES[-1]
        else:
            self.hero.activeHeroClass = CLASSES[i-1]
    def changeClassRight(self):
        i = CLASSES.index(self.hero.getActiveHeroClass())
        if i == len(CLASSES) -1:
            self.hero.activeHeroClass = CLASSES[0]
        else:
            self.hero.activeHeroClass = CLASSES[i+1]
    def makeText(self, text):
        return self.textFont.render(text, True, (0,0,0))
    def previousSurface(self):
        self.ismain = False
    def mainLoop(self):
        while self.ismain == True:
            self.draw(self.surface)
            self.eventLoop()
            pygame.display.update()
    def eventLoop(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if self.leftClassButton.getRect().collidepoint(event.pos):
                    self.leftClassButton.callBack()
                if self.rightClassButton.getRect().collidepoint(event.pos):
                    self.rightClassButton.callBack()
                if self.quitButton.getRect().collidepoint(event.pos):
                    self.quitButton.callBack()
                if self.meleeButton.getRect().collidepoint(event.pos):
                    self.meleeButton.callBack()
                if self.rangedButton.getRect().collidepoint(event.pos):
                    self.rangedButton.callBack()
                if self.armorButton.getRect().collidepoint(event.pos):
                    self.armorButton.callBack()
                if self.shieldButton.getRect().collidepoint(event.pos):
                    self.shieldButton.callBack()
                for x in self.weaponButtons:
                    if x.getRect().collidepoint(event.pos):
                        x.callBack()
                        self.weaponButtons = []
            if event.type == QUIT:
                pygame.quit()
    def assignMeleeWeapon(self, w):
        self.hero.meleeWeapon = w
    def assignRangedWeapon(self, r):
        self.hero.rangedWeapon = r
    def assignArmor(self, a):
        self.hero.armor = a
    def assignShield(self, s):
        self.hero.shield = s
    def drawEquipmentComponent(self, surface):
        self.meleeButton.draw(surface)
        self.rangedButton.draw(surface)
        self.armorButton.draw(surface)
        self.shieldButton.draw(surface)
        i = 0
        for x in self.weaponButtons:
            x.setRect(pygame.Rect(500, i, 100, 50))
            x.draw(surface)
            i = i + 50 
    def makeStatsComponent(self, surface):
        self.rangedButton = multilinetextbutton.MultiLineTextButton([self.makeText("Ranged Equipped:"), self.makeText(self.hero.getRangedWeapon().getName())], self.makeRangedUI, rect = pygame.Rect(600, 150, 200, 100))
        self.armorButton = multilinetextbutton.MultiLineTextButton([self.makeText("Armor Equipped: "), self.makeText(self.hero.getArmor().getName())], self.makeArmorUI, rect = pygame.Rect(600, 250, 200, 100))
        self.shieldButton = multilinetextbutton.MultiLineTextButton([self.makeText("Shield Equipped:"), self.makeText(self.hero.getShield().getName())], self.makeShieldUI, rect = pygame.Rect(600, 350, 200, 100))
        self.meleeButton = multilinetextbutton.MultiLineTextButton([self.makeText("Melee Equipped:"), self.makeText(self.hero.getMeleeWeapon().getName())], self.makeMeleeUI, rect = pygame.Rect(600, 50, 200, 100))
        self.heroClassLabel = pygame.font.Font(pygame.font.get_default_font(), 34).render(self.hero.getActiveHeroClass().getName(), True, (0,0,0))
        surface.blit(self.nameLabel, pygame.Rect(10,10, self.nameLabel.get_rect().width, self.nameLabel.get_rect().height))
        surface.blit(self.levelLabel, pygame.Rect(10 + self.nameLabel.get_rect().width + 15,10, self.nameLabel.get_rect().width, self.nameLabel.get_rect().height))
        racerect = self.raceLabel.get_rect()
        racerect.center = self.nameLabel.get_rect().center
        racerect.y = racerect.y + 40
        surface.blit(self.raceLabel, racerect)
        self.professionRect = pygame.Rect(10, 100, self.professionLabel.get_rect().width,self.professionLabel.get_rect().height)
        surface.blit(self.professionLabel, self.professionRect)
        self.heroClassRect = pygame.Rect(100, self.professionLabel.get_rect().height + self.professionRect.y + 10, self.heroClassLabel.get_rect().width,self.heroClassLabel.get_rect().height)
        surface.blit(self.heroClassLabel, self.heroClassRect)
        self.leftClassButton.setRect(pygame.Rect(self.heroClassRect.x - 50, self.heroClassRect.y, 35,38))
        self.rightClassButton.setRect(pygame.Rect(self.heroClassRect.x + self.heroClassRect.width + 15, self.heroClassRect.y, 35,38))
        self.leftClassButton.draw(surface)
        self.rightClassButton.draw(surface)
        surface.blit(self.strLabel, pygame.Rect(self.professionRect.x, self.heroClassRect.y + 50, self.strLabel.get_rect().width, self.strLabel.get_rect().height))
        surface.blit(self.agiLabel, pygame.Rect(self.professionRect.x, self.heroClassRect.y + 70, self.agiLabel.get_rect().width, self.agiLabel.get_rect().height))
        surface.blit(self.conLabel, pygame.Rect(self.professionRect.x, self.heroClassRect.y + 90, self.conLabel.get_rect().width, self.conLabel.get_rect().height))
        surface.blit(self.intLabel, pygame.Rect(self.professionRect.x, self.heroClassRect.y + 110, self.intLabel.get_rect().width, self.intLabel.get_rect().height))
        surface.blit(self.wisLabel, pygame.Rect(self.professionRect.x, self.heroClassRect.y + 130, self.wisLabel.get_rect().width, self.wisLabel.get_rect().height))
    def drawComponents(self, surface):
        self.makeStatsComponent(surface)
        self.drawEquipmentComponent(surface)
    def draw(self, surface):
        surface.fill((0,0,0))
        pygame.draw.rect(surface, self.backgroundColor, pygame.Rect(2,2,796, 796))  
        self.drawComponents(surface)
        self.quitButton.draw(surface)
