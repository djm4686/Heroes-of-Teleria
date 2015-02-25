import pygame, party, button, activeHeroEvent, targetevent, battlepartymanager, zoneevent, random, imageevent, herostatusevent, moveanimation, phase, herobattlestats, moveevent
import isoboard
from pygame.locals import *
import sys
import ai
import textanimation



class BattleScene:
    def __init__(self, surface, party1 = party.getAi(), party2 = party.getAi(), aion = True):
        pygame.init()
        self.party1 = party1
        self.party2 = party2
        self.me = self.party1
        self.phase = phase.Phase("Placement")
        self.phase.addSubPhase(phase.Phase("Placement"))
        self.phaseCount = 0
        self.order = []
        self.surface = surface
        self.determineInitiative()
        self.aion = aion
        self.ai = ai.AIBehavior(self.party2)
        self.heroAnimation = None
        self.ismain = True
        self.backButton = button.Button(self.makeText("Back"))
        self.events = []
        self.moving = False
        self.playerTurn = False
        self.moved = False
        self.attacked = False
        self.originp = (0,0)
        self.animations = []
        self.mouseOver = None
        self.hexBoard = isoboard.IsoBoard(10,10, 64)
        self.makeChoiceButtons()
        self.cancelButton = button.Button(self.makeText("Cancel"), self.startPhase)
        self.cancelButton.setRect(pygame.Rect(200, 550, 100, 50))
        self.endTurnButton = button.Button(self.makeText("End Turn"), self.nextHero)
        self.endTurnButton.setRect(pygame.Rect(700, 550, 100, 50))
        self.initVars()
        self.mainLoop()
    def initVars(self):
        self.partyManager = battlepartymanager.BattlePartyManager(self.party1, self.party2)
    def getEvent(self, ide):
        for x in self.events:
            if x.getID() == ide:
                return x

    def isDead(self, hero):
        l = [] + self.order
        if hero.isDead():
            for x in range(len(self.order)):
                if self.order[x].getID() == hero.getID():
                    l.pop(x)
                    if self.phaseCount >= len(self.order):
                        self.phaseCount = 0
        self.order = l

    def meleePhase(self):
        self.phase.addSubPhase(phase.Phase("Melee"))
        self.events = []

    def rangedPhase(self):
        self.phase.addSubPhase(phase.Phase("Ranged"))
        self.events = []

    def skillPhase(self):
        self.phase.addSubPhase(phase.Phase("Skill"))
        self.events = []

    def movePhase(self):
        if self.moved == False:
            self.phase.addSubPhase(phase.Phase("Move"))
            self.events = []

    def attackPhase(self):
        if self.attacked == False:
            self.phase.addSubPhase(phase.Phase("Attack"))
            self.events = []
            self.makeAttackButtons()

    def startPhase(self):
        self.phase.addSubPhase(phase.Phase("TurnStart"))
        self.events = []
        self.makeChoiceButtons()

    def makeAttackButtons(self):
        self.choiceButtons = []
        self.choiceButtons.append(button.Button(self.makeText("Melee"), self.meleePhase))
        self.choiceButtons.append(button.Button(self.makeText("Ranged"), self.rangedPhase))
        self.choiceButtons.append(button.Button(self.makeText("Skill"), self.skillPhase))

    def makeChoiceButtons(self):
        self.choiceButtons = []
        self.choiceButtons.append(button.Button(self.makeText("Move"), self.movePhase))
        self.choiceButtons.append(button.Button(self.makeText("Attack"), self.attackPhase))

    def resetPhase(self):
        self.phaseCount = 0
        self.events = []

    def nextHero(self):
        self.moved = False
        self.attacked = False
        if self.phaseCount == len(self.order) - 1:
            self.phaseCount = 0
        else:
            self.phaseCount = self.phaseCount + 1

    def addEvent(self, event):
        for x in range(len(self.events)):
            if self.events[x].getID() == event.getID():
                self.events[x] = event
        self.events.append(event)

        return True
    def mainLoop(self):
        while self.ismain:
            self.update()
            self.eventLoop()
            self.draw(self.surface)
            pygame.display.update()
        for x in self.party1.getHeroes() + self.party2.getHeroes():
            x.setTile(None)
            x.resetHP()
    def getTilesWithRange(self, rang, tile):
        tiles = [tile]
        temptiles = [tile]
        currtile = tile
        i = 0
        while rang - i > 1:
            for t in tiles:
                for x in t.getNeighbors():
                    if x!= None and x.getGameObject() == None:
                        temptiles.append(x)
            
            tiles = [] + temptiles    
            i = i + 1
        return tiles

    def animationPhase(self):
        self.phase.addSubPhase(phase.Phase("Animation"))

    def chooseTile(self, activeTile):
        self.events = []
        activeTile.setGameObject(self.getActiveHero())
        self.phase.addSubPhase(phase.Phase("Direction"))
        if self.phaseCount >= len(self.order):
            self.resetPhase()
            self.phase = phase.Phase("Main")
            self.phase.addSubPhase(phase.Phase("TurnStart"))

    def chooseDirection(self, pos):
        self.hexBoard.setDirection(self.getActiveHero(), pos)
        self.phase.addSubPhase(phase.Phase("Placement"))
        self.phaseCount += 1
        if self.phaseCount >= len(self.order):
                self.resetPhase()
                self.phase = phase.Phase("Main")
                self.phase.addSubPhase(phase.Phase("TurnStart"))
    def enemyTurn(self):
        if self.aion:
            ts = self.hexBoard.getZone2()
            r = ts[random.randrange(0, len(ts))]
            while r.getGameObject() != None:
                r = ts[random.randrange(0, len(ts))]
            activeTile = r
            activeTile.setGameObject(self.getActiveHero())
            self.phaseCount += 1
            if self.phaseCount >= len(self.order):
                    self.resetPhase()
                    self.phase = phase.Phase("Main")
                    self.phase.addSubPhase(phase.Phase("TurnStart"))
    def eventLoop(self, player1ID = 1, player2ID = 2):
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()

            if event.type == MOUSEMOTION:
                t = self.hexBoard.collidepoint(event.pos)
                if t != None and t.getGameObject() != None:
                    self.mouseOver = t.getGameObject()
                else:
                    self.mouseOver = None
            if self.phase.getSubPhase().getName() == "Animation":
                return
            if event.type == MOUSEMOTION and self.moving == True:
                self.hexBoard.setNewCoords((event.pos[0] - self.originp[0], event.pos[1] - self.originp[1]))
                self.originp = event.pos
            if event.type == MOUSEBUTTONDOWN and event.button == 3:
                self.moving = True
                self.originp = event.pos
            if event.type == MOUSEBUTTONDOWN and event.button == 2:
                activeTile = self.hexBoard.collidepoint(event.pos)
                if activeTile is not None:
                    t = self.hexBoard.getNeighborTiles(activeTile, 3)
                    self.addEvent(zoneevent.ZoneEvent(5, t))
            if event.type == MOUSEBUTTONUP and event.button == 3:
                self.moving = False
            if event.type == MOUSEBUTTONUP and event.button == 1 and self.backButton.getRect().collidepoint(event.pos):
                self.ismain = False
            if self.phase.getName() == "Placement":
                if self.phase.getSubPhase().getName() == "Direction":
                    self.addEvent(activeHeroEvent.activeHeroEvent(0, self.getActiveHero().getTile()))
                    if event.type == MOUSEMOTION:
                        self.hexBoard.setDirection(self.getActiveHero(), event.pos)
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        self.chooseDirection(event.pos)
                elif self.phase.getSubPhase().getName() == "Placement":
                    if self.partyManager.checkHero(self.getActiveHero()) == player2ID:
                        self.enemyTurn()
                    if self.partyManager.checkHero(self.getActiveHero()) == player1ID:
                        self.addEvent(zoneevent.ZoneEvent(101, self.hexBoard.getZone1()))
                    activeTile = None
                    if event.type == MOUSEMOTION:
                        activeTile = self.hexBoard.collidepoint(event.pos)

                        if activeTile != None and activeTile.getZone() == self.partyManager.checkHero(self.getActiveHero()):
                            self.addEvent(activeHeroEvent.activeHeroEvent(0, activeTile))
                            self.addEvent(imageevent.ImageEvent(200, self.getActiveHero().getActiveHeroClass().getSprite(), activeTile))
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        activeTile = self.hexBoard.collidepoint(event.pos)
                        if activeTile != None and activeTile.getGameObject() == None and activeTile.getZone() == self.partyManager.checkHero(self.getActiveHero()):
                            self.chooseTile(activeTile)
            elif self.phase.getName() == "Main":
                if self.attacked == True and self.moved == True:
                    self.nextHero()
                self.events = []
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.endTurnButton.collidepoint(event.pos):
                    self.endTurnButton.callBack()
                for x in range(len(self.order)):
                        if self.partyManager.checkHero(self.order[x]) == 1:
                            self.addEvent(herostatusevent.HeroStatusEvent(10 + x, self.order[x].getTile()))
                        else:
                            self.addEvent(herostatusevent.HeroStatusEvent(10 + x, self.order[x].getTile(), (205,14,38)))
                if self.phase.getSubPhase().getName() == "TurnStart":
                    if self.partyManager.checkHero(self.getActiveHero()) == 1:
                        self.playerTurn = True
                        for x in self.choiceButtons:
                            if event.type == MOUSEBUTTONUP and x.collidepoint(event.pos):
                                x.callBack()
                    else:
                        pass
                elif self.phase.getSubPhase().getName() == "Move":
                    self.addEvent(moveevent.MoveEvent(200, self.getActiveHero().getTile(), self.getActiveHero().getMovementRange()))
                    for x in self.getTilesWithRange(self.getActiveHero().getMovementRange(), self.getActiveHero().getTile()):
                        if event.type == MOUSEBUTTONUP and event.button == 1 and x.collidepoint(event.pos) and not self.cancelButton.collidepoint(event.pos) and not self.backButton.collidepoint(event.pos):
                            self.processMove(x)
                elif self.phase.getSubPhase().getName() == "Attack":
                    for x in self.choiceButtons:
                        if event.type == MOUSEBUTTONUP and x.collidepoint(event.pos):
                            x.callBack()
                elif self.phase.getSubPhase().getName() == "Melee":
                    self.addEvent(targetevent.TargetEvent(2, self.getActiveHero().getTile(), 2, (255,0,0)))
                    for x in self.getEvent(2).getTiles():
                        if event.type == MOUSEBUTTONUP and event.button == 1 and x.collidepoint(event.pos) and x.getGameObject() != None:
                            self.processMeleeAttack(self.getActiveHero(), x.getGameObject())
                elif self.phase.getSubPhase().getName() == "Ranged":
                    self.addEvent(targetevent.TargetEvent(2, self.getActiveHero().getTile(),self.getActiveHero().getRangedRange(), (255,0,0)))
                    for x in self.getEvent(2).getTiles():
                        if event.type == MOUSEBUTTONUP and event.button == 1 and x.collidepoint(event.pos) and x.getGameObject() != None:
                            self.processRangedAttack(self.getActiveHero(), x.getGameObject())
                if self.phase.getSubPhase().getName() != "TurnStart":
                    if event.type == MOUSEBUTTONUP and self.cancelButton.collidepoint(event.pos):
                        self.cancelButton.callBack()
                if self.checkForWinner():
                    self.addEvent(activeHeroEvent.activeHeroEvent(0, self.getActiveHero().getTile()))
            elif self.phase.getName() == "test":
                if event.type == MOUSEMOTION:
                    tile = self.hexBoard.collidepoint(event.pos)
                    if tile != None:
                        self.addEvent(targetevent.TargetEvent(tile, 2))

    def processMove(self, tile):
        self.heroAnimation = moveanimation.MoveAnimation(self.getActiveHero().getTile(), tile, self.getActiveHero())
        self.animationPhase()
        self.events = []
        self.moved = True
    def processRangedAttack(self, attacker, defender):
        attacker.rangedAttack(defender)
        self.attacked = True
        self.isDead(defender)
        self.startPhase()
    def processMeleeAttack(self, attacker, defender):
        dmg = attacker.meleeAttack(defender)
        self.attacked = True
        self.isDead(defender)
        self.startPhase()
        self.animations.append(textanimation.TextAnimation(str(dmg) + " Damage!", defender.getTile().getCenter()))
    def getActiveHero(self):
        return self.order[self.phaseCount]
    def update(self):
        if self.phase.getSubPhase().getName() == "TurnStart" and self.partyManager.checkHero(self.getActiveHero()) != 1:
            self.processAITurn(*self.ai.processTurn(self.hexBoard, self.getActiveHero(), self.moved, self.attacked))
        self.checkForWinner()
        if self.p1Dead:
            self.ismain = False
        if self.p2Dead:
            self.ismain = False
    def processAITurn(self, command, value):
        if self.attacked == True and self.moved == True:
            if not self.checkForWinner():
                self.nextHero()
            return
        if command == "Move":
            self.processMove(value)
        elif command == "MeleeAttack":
            self.processMeleeAttack(self.getActiveHero(), value.getGameObject())
        elif command == "End":
            self.nextHero()

    def checkForWinner(self):
        self.p1Dead = True
        self.p2Dead = True
        for x in self.party1.getHeroes():
            if not x.isDead():
                self.p1Dead = False
        for x in self.party2.getHeroes():
            if not x.isDead():
                self.p2Dead = False
        return self.p1Dead or self.p2Dead
    def drawPhase(self):
        pass
    def drawActiveHero(self, surface):
        h = self.getActiveHero()
        if self.mouseOver != None:
            b = herobattlestats.HeroBattleStats(self.mouseOver)
        else:
            b = herobattlestats.HeroBattleStats(h)
        b.draw(surface)
    def makeText(self, text):
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
        return self.font.render(text, True, (0,0,0))
    def determineInitiative(self):
        for x in self.party1.getHeroes() + self.party2.getHeroes():
            self.order.append(x)
        random.shuffle(self.order)
        while True:
            i = 0
            for x in range(len(self.order)):
                if x != len(self.order) - 1:
                    if self.order[x].getInitiative() < self.order[x + 1].getInitiative():
                        h1 = self.order[x]
                        h2 = self.order[x + 1]
                        self.order[x] = h2
                        self.order[x+1] = h1
                        i = 1
            if i == 0:
                break
        self.activeHero = self.order[0]
    def draw(self, surface):
        surface.fill((128, 128, 128))
        self.backButton.setRect(pygame.Rect(700,0,100,50))
        
        self.hexBoard.drawTiles(surface)
        if not self.checkForWinner():
            self.drawActiveHero(surface)
        self.backButton.draw(surface)
        for x in self.events:
            if x.getID() < 100:
                x.draw(surface)
        for x in self.events:
            if x.getID() > 100:
                x.draw(surface)
        if self.phase.getName() == "Main":
            if self.phase.getSubPhase().getName() != "TurnStart":
                self.cancelButton.draw(surface)
            if self.phase.getSubPhase().getName() == "TurnStart":
                for x in range(len(self.choiceButtons)):
                    self.choiceButtons[x].setRect(pygame.Rect(200, 400 + (x * 50), 100, 50))
                    self.choiceButtons[x].draw(surface)
            elif self.phase.getSubPhase().getName() == "Attack":
                for x in range(len(self.choiceButtons)):
                    self.choiceButtons[x].setRect(pygame.Rect(200, 400 + (x * 50), 100, 50))
                    self.choiceButtons[x].draw(surface)
            if self.phase.getSubPhase().getName() == "Animation" and self.heroAnimation != None and self.heroAnimation.working == True:
                if self.getActiveHero().getTile() != None:
                    self.getActiveHero().draw(surface, True)
                node = self.heroAnimation.animate(surface)
                if node != None:
                    print node.getID()
                    for x in range(len(self.hexBoard.tiles)):
                        for y in range(len(self.hexBoard.tiles[x])):
                            if self.hexBoard.tiles[x][y].getID() == node.getID():
                                print self.getActiveHero().getName()
                                self.hexBoard.tiles[x][y].setGameObject(self.getActiveHero())
                                self.hexBoard.tiles[x][y].getGameObject().draw(surface)
                                self.heroAnimation = None
                                self.startPhase()
            self.endTurnButton.draw(surface)
        self.hexBoard.drawHeroes(surface)
        for x in self.animations:
            if not x.animate(surface):
                self.animations.remove(x)
        
if __name__ == "__main__":
    pygame.init()
    b = BattleScene(pygame.display.set_mode((800,600)))
