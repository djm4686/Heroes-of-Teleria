import pygame, hero, human, party, button, imagebutton, random, ast, battlescene, socket, networking, lobbyscene
from globalvars import *
from pygame.locals import *
class HeroCreationScreen():
    def __init__(self, surface, player):
        self.textColor = (0,0,0)
        self.player = player
        self.backgroundColor = (128,128,128)
        self.surface = surface
        self.keysPressed = []
        self.ismain = True
        self.heroes = 0
        self.initVariables()
        self.getAllHeroes()
        self.mainLoop()
    def initVariables(self):
        self.party = party.Party(self.player)
        self.bgimage = pygame.transform.scale2x(pygame.image.load("images/panel_blue.png"))
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.addHeroButton = button.Button(self.makeText("Add Hero"), self.addHero)
        self.addHeroButton.setRect(pygame.Rect(700, 550, 100, 50))
        self.toBattleButton = button.Button(self.makeText("To Lobbies"))
        self.toBattleButton.setRect(pygame.Rect(600,550,100,50))
    def addHero(self):
        h = self.makeHero()
        self.sendHeroToDB(h)
        self.party.addHero(h)
    def getAllHeroes(self):
        HOST, PORT = "localhost", 9999
        data = networking.DataFrame(networking.Header(1, "getHeroes"), {"playerID" : str(self.player.getID())}).toString()

        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(data + "\n")

            # Receive data from the server and shut down
            received = sock.recv(4096)
        finally:
            sock.close()
        received = ast.literal_eval(received)
        if received["header"]["reqtype"] == "heroes":
            for heroJSON in received["data"]["heroes"]:
                j = ast.literal_eval(heroJSON)
                self.party.addHero(hero.createFromJSON(j))
            self.error = False
        else:
            self.error = True
        
    def makeText(self, text):
        return self.font.render(text, True, self.textColor)
    def sendHeroToDB(self, hero):
        HOST, PORT = "localhost", 9999
        data = networking.DataFrame(networking.Header(1, "createHero"), {"playerID" : str(self.player.getID()), "hero" : ast.literal_eval(hero.getJSON())}).toString()

        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(data + "\n")

            # Receive data from the server and shut down
            received = sock.recv(1024)
        finally:
            sock.close()
        received = ast.literal_eval(received)
        if received["header"]["reqtype"] == "success":
            print received["data"]["heroID"]
            hero.setID(int(received["data"]["heroID"]))
            self.error = False
        else:
            self.error = True
    def makeHero(self):
        h = hero.Hero(self.heroes, random.choice(NAMES), heroclass = random.choice(CLASSES), race = random.choice(RACES))
        
        self.heroes = self.heroes + 1
        return h
    def eventHandler(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                pass
            if event.type == MOUSEBUTTONUP and event.button == 1:
                mx, my = event.pos
                if len(self.keysPressed)> 0:
                    self.keysPressed.pop()
                if self.addHeroButton.getRect().collidepoint(event.pos):
                    self.addHeroButton.callBack()
                elif self.toBattleButton.getRect().collidepoint(event.pos):
                    b = lobbyscene.LobbyScene(self.surface, self.player, self.party)
                else:
                    for x in range(len(self.nameButtons)):
                        if self.nameButtons[x].getRect().collidepoint((mx,my)) and not self.levelUpButtons[x].getRect().collidepoint((mx,my)):
                            self.nameButtons[x].callBack()
                        elif self.levelUpButtons[x].getRect().collidepoint((mx,my)):
                            self.levelUpButtons[x].callBack()
            if event.type == QUIT:
                pygame.quit()
    def mainLoop(self):
        while self.ismain == True:
            self.createUI()
            self.update()
            self.draw(self.surface)
            self.eventHandler()
            pygame.display.update()
    def update(self):
        pass
                        
    def createUI(self):
        self.bgImages = []
        self.nameButtons = []
        self.hpLabels = []
        self.raceLabels = []
        self.activeClassLabels = []
        self.levelLabels = []
        self.strLabels = []
        self.agiLabels = []
        self.conLabels = []
        self.intLabels = []
        self.wisLabels = []
        self.levelUpButtons = []
        self.manaLabels = []
        for hero in self.party.getHeroes():
            self.bgImages.append(imagebutton.ImageButton(self.bgimage, None))
            b = button.Button(self.makeText(hero.getName()),hero.makeConfigScreen, [self.surface])
            b.setRect(pygame.Rect(0,0, 100, 20))
            self.nameButtons.append(b)
            self.manaLabels.append(self.makeText("Max Mana: " + str(hero.getMaxMana())))
            self.hpLabels.append(self.makeText("Max HP: " + str(hero.getMaxHp())))
            self.raceLabels.append(self.makeText("Race: " + hero.getRace().getName()))
            self.activeClassLabels.append(self.makeText("Profession: " + hero.getActiveHeroClass().getName()))
            self.levelLabels.append(self.makeText("Lvl: " + str(hero.getLevel())))
            self.strLabels.append(self.makeText("Str: " + str(hero.getStr())))
            self.agiLabels.append(self.makeText("Agi: " + str(hero.getAgi())))
            self.conLabels.append(self.makeText("Con: " + str(hero.getCon())))
            self.intLabels.append(self.makeText("Int: " + str(hero.getInt())))
            self.wisLabels.append(self.makeText("Wis: " + str(hero.getWis())))
            self.levelUpButtons.append(button.Button(self.makeText("Level Up"), callBack = hero.levelUp))
    def drawUI(self, surface):
        row = 0
        for x in range(len(self.nameButtons)):
            if x != 0  and 800 / (x - (row * 4)) <= 200:
                row = row + 1
            self.levelUpButtons[x].setRect(pygame.Rect((x - (row * 4)) * 200 + 100, row * 200 + 145, 75, 40))
            self.bgImages[x].setRect(pygame.Rect((x - (row * 4)) * 200, row * 200, 200, 200))
            for e in self.keysPressed:
                if self.bgImages[x].getRect().collidepoint(e.pos) and not self.levelUpButtons[x].getRect().collidepoint(e.pos):
                    self.bgImages[x].image = pygame.transform.scale(pygame.image.load("images\panelInset_blue.png"), (200,200))
            self.bgImages[x].draw(surface)
            self.nameButtons[x].setRect(pygame.Rect((x - (row * 4)) * 200 + 10, row * 200 + 10, 75, 20))
            self.nameButtons[x].draw(surface)
            surface.blit(self.raceLabels[x], pygame.Rect((x - (row * 4)) * 200 + 10, row * 200 + 35, 150, 20))
            surface.blit(self.activeClassLabels[x], pygame.Rect((x - (row * 4)) * 200 + 10, row * 200 + 50, 150, 20))
            surface.blit(self.hpLabels[x], pygame.Rect((x - (row * 4)) * 200 + 10, row * 200 + 70, 150, 20))
            surface.blit(self.manaLabels[x], pygame.Rect((x - (row * 4)) * 200 + 10, row * 200 + 85, 150, 20))
            surface.blit(self.levelLabels[x], pygame.Rect((x - (row * 4)) * 200 + 140, row * 200 + 10, 150, 20))
            surface.blit(self.strLabels[x], pygame.Rect((x - (row * 4)) * 200 + 10, row * 200 + 100, 150, 20))
            surface.blit(self.agiLabels[x], pygame.Rect((x - (row * 4)) * 200 + 10, row * 200 + 115, 150, 20))
            surface.blit(self.conLabels[x], pygame.Rect((x - (row * 4)) * 200 + 10, row * 200 + 130, 150, 20))
            surface.blit(self.intLabels[x], pygame.Rect((x - (row * 4)) * 200 + 10, row * 200 + 145, 150, 20))
            surface.blit(self.wisLabels[x], pygame.Rect((x - (row * 4)) * 200 + 10, row * 200 + 160, 150, 20))
            self.levelUpButtons[x].draw(surface)
        self.addHeroButton.draw(surface)
        self.toBattleButton.draw(surface)
    def draw(self, surface):
        surface.fill(self.backgroundColor)
        self.drawUI(surface)
if __name__ == "__main__":
    pygame.init()
    h = HeroCreationScreen(pygame.display.set_mode((800,600)))
