import pygame, party, button, activeHeroEvent, targetevent, battlepartymanager, zoneevent, random, imageevent, herostatusevent, moveanimation, phase, herobattlestats, moveevent
import isoboard
from pygame.locals import *
import ai
import textanimation
import endstatslayer
import cloud
import time
import choicebox

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
        self.lastTime = time.clock()
        self.centered = False
        self.surface = surface
        self.determineInitiative()
        self.battleStatsI = 0
        self.aion = aion
        self.ai = ai.AIBehavior(self.party2)
        self.heroAnimation = None
        self.ismain = True
        self.backButton = button.Button(self.makeText("Back"))
        self.events = []
        self.moving = False
        self.playerTurn = False
        self.moved = False
        self.clouds = []
        self.populateBackground()
        self.attacked = False
        self.choiceBox = choicebox.ChoiceBox(155,self.surface.get_rect().height - 100)
        self.originp = (0,0)
        self.animations = []
        self.mouseOver = None
        self.currentSpell = None
        self.drawToolTip = False
        self.toolTipPos = None
        self.hexBoard = isoboard.IsoBoard(10,10, 64)
        self.makeChoiceButtons()
        self.cancelButton = button.Button(self.makeText("Cancel"), self.startPhase)
        self.cancelButton.setRect(pygame.Rect(200, 550, 100, 50))
        self.endTurnButton = button.Button(self.makeText("End Turn"), self.nextHero)
        self.endTurnButton.setRect(pygame.Rect(700, 550, 100, 50))
        self.emitter = None
        self.initVars()
        self.mainLoop()
    def initVars(self):
        self.partyManager = battlepartymanager.BattlePartyManager(self.party1, self.party2)
    def getEvent(self, ide):
        for x in self.events:
            if x.getID() == ide:
                return x
    def centerCamera(self, tile):
        center = tile.getCenter()
        startx = center[0]
        starty = center[1]
        endx = 400
        endy = 300

        self.hexBoard.setNewCoords((endx - startx, endy - starty))
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
        self.makeAttackTypeChoice()

    def rangedPhase(self):
        self.phase.addSubPhase(phase.Phase("Ranged"))
        self.events = []
        self.makeAttackTypeChoice()
    def skillPhase(self):
        self.phase.addSubPhase(phase.Phase("Skill"))
        self.events = []

    def movePhase(self):
        if self.moved == False:
            self.phase.addSubPhase(phase.Phase("Move"))
            self.events = []
            self.makeMoveChoice()

    def attackPhase(self):
        if self.attacked == False:
            self.phase.addSubPhase(phase.Phase("Attack"))
            self.events = []
            self.makeAttackButtons()

    def startPhase(self):
        self.phase.addSubPhase(phase.Phase("TurnStart"))
        self.events = []
        self.makeChoiceButtons()
        self.centered = False

    def makeAttackButtons(self):
        self.choiceBox.clearChoices()
        self.choiceBox.addChoice(self.makeText("Melee"), self.meleePhase, "Melee Attack", "Make an attack to an adjacent Hero.")
        self.choiceBox.addChoice(self.makeText("Ranged"), self.rangedPhase, "Ranged Attack", "Make an attack to a hero within range of your Ranged Weapon.")
        self.choiceBox.addChoice(self.makeText("Cancel"), self.startPhase, "Cancel", "Go back to the previous menu.")
        #self.choiceButtons.append(button.Button(self.makeText("Skill"), self.skillPhase, tooltipName=""))
    def makeMoveChoice(self):
        self.choiceBox.clearChoices()
        self.choiceBox.addChoice(self.makeText("Cancel"), self.startPhase, "Cancel", "Go back to the previous menu.")
    def makeAttackTypeChoice(self):
        self.choiceBox.clearChoices()
        self.choiceBox.addChoice(self.makeText("Cancel"), self.startPhase, "Cancel", "Go back to the previous menu.")
    def makeChoiceButtons(self):
        self.choiceBox.clearChoices()
        self.choiceBox.addChoice(self.makeText("Move"), self.movePhase, "Move Command", "Move this hero to another tile. This can only be done once per turn.")
        self.choiceBox.addChoice(self.makeText("Attack"), self.attackPhase, "Attack Command", "Have this Hero attack another. This can only be done once per turn.")
        self.choiceBox.addChoice(self.makeText("Spell"), self.spellPhase, "Spell Command", "Have this hero cast a Spell upon another. This can only be done once per turn.")
        self.choiceBox.addChoice(self.makeText("End Turn"), self.endTurn, "End Turn", "End your turn! Duh!")
    def makeSpellButtons(self):
        self.choiceBox.clearChoices()
        self.choiceBox.addChoice(self.makeText(self.getActiveHero().getMeleeWeapon().getSpell().getName()),
                                                self.getSpellTarget, self.getActiveHero().getMeleeWeapon().getSpell().getName(),
                                                self.getActiveHero().getMeleeWeapon().getSpell().getDescription(),
                                                [self.getActiveHero().getMeleeWeapon().getSpell()])
        self.choiceBox.addChoice(self.makeText("Cancel"), self.startPhase, "Cancel", "Go back to the previous menu.")
    def endTurn(self):
        self.moved = False
        self.attacked = False
        self.phase.addSubPhase(phase.Phase("EndTurn"))
    def getSpellTarget(self, spell):
        self.phase.addSubPhase(phase.Phase("TargetSpell"))
        self.currentSpell = spell
        self.makeAttackTypeChoice()

    def spellPhase(self):
        if not self.attacked:
            self.phase.addSubPhase(phase.Phase("Spell"))
            self.makeSpellButtons()

    def resetPhase(self):
        self.phaseCount = 0
        self.events = []
    def syncBoard(self):
        pass
        # for row in self.hexBoard.tiles:
        #     for cell in row:
        #         if cell.getGameObject() != None:
        #             for x in range(len(self.order)):
        #                 if cell.getGameObject().getID() == self.order[x].getID():
        #                     self.order[x] = cell.getGameObject()
    def nextHero(self):
        self.moved = False
        self.attacked = False
        self.getActiveHero().attacked = False
        self.getActiveHero().moved = False
        for x in self.order:
            x.updateSpellEffectsTurn()
            x.updateModifyers()
        if self.phaseCount == len(self.order) - 1:
            self.phaseCount = 0
        else:
            self.phaseCount = self.phaseCount + 1
        self.getActiveHero().updateSpellEffectsRound()

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
            if self.checkForWinner():
                    stats = endstatslayer.Stats([100,100], self.party1, self.party2, "Game Over!")
                    while stats.is_main:
                        stats.eventLoop()
                        stats.draw(self.surface)
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
    def removeEvent(self, id):
        for x, i in zip(self.events, range(len(self.events))):
            if x.id == id:
                self.events.pop(i)
                break
    def eventLoop(self, player1ID = 1, player2ID = 2):
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
            if event.type == MOUSEMOTION and self.partyManager.checkHero(self.getActiveHero()) == 1:
                self.choiceBox.clearHighlights()
                choice = self.choiceBox.collidepoint(event.pos)
                if choice != None:
                    choice.mouseOver()
            if event.type == MOUSEMOTION:
                if self.phase.getName() != "Placement" and self.phase.getSubPhase().getName() != "Animation":
                    for x in self.order:
                        if x.collidepoint(event.pos):
                            print "mousing over"
                            x.selected = True
                            self.mouseOver = x
                            break
                        else:
                            x.selected = False
                            self.mouseOver = None

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
                    self.addEvent(activeHeroEvent.activeHeroEvent(2000, self.getActiveHero().getTile()))
                    if event.type == MOUSEMOTION:
                        self.hexBoard.setDirection(self.getActiveHero(), event.pos)
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        self.chooseDirection(event.pos)
                elif self.phase.getSubPhase().getName() == "Placement":
                    if self.partyManager.checkHero(self.getActiveHero()) == player2ID:
                        self.enemyTurn()
                    if self.partyManager.checkHero(self.getActiveHero()) == player1ID:
                        self.addEvent(zoneevent.ZoneEvent(22, self.hexBoard.getZone1()))
                    activeTile = None
                    if event.type == MOUSEMOTION:
                        activeTile = self.hexBoard.collidepoint(event.pos)

                        if activeTile != None and activeTile.getZone() == self.partyManager.checkHero(self.getActiveHero()):
                            self.addEvent(activeHeroEvent.activeHeroEvent(10000, activeTile))
                            self.addEvent(imageevent.ImageEvent(200, self.getActiveHero().getActiveHeroClass().getSprite(), activeTile))
                        if activeTile == None:
                            self.removeEvent(200)
                            self.removeEvent(0)
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        activeTile = self.hexBoard.collidepoint(event.pos)
                        if activeTile != None and activeTile.getGameObject() == None and activeTile.getZone() == self.partyManager.checkHero(self.getActiveHero()):
                            self.chooseTile(activeTile)
            elif self.phase.getName() == "Main":
                if self.attacked == True and self.moved == True:
                    self.nextHero()
                self.events = []
                #if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.endTurnButton.collidepoint(event.pos):
                #    self.endTurnButton.callBack()
                for x in range(len(self.order)):
                        if self.partyManager.checkHero(self.order[x]) == 1:
                            self.addEvent(herostatusevent.HeroStatusEvent(10 + x, self.order[x].getTile()))
                        else:
                            self.addEvent(herostatusevent.HeroStatusEvent(10 + x, self.order[x].getTile(), (205,14,38)))
                if self.phase.getSubPhase().getName() == "TurnStart":
                    if not self.centered:
                        self.hexBoard.centerCamera(self.getActiveHero().getTile())
                        self.centered = True
                    if self.partyManager.checkHero(self.getActiveHero()) == 1:
                        self.playerTurn = True
                        if event.type == MOUSEBUTTONUP:
                            choice = self.choiceBox.collidepoint(event.pos)
                            if choice:
                                choice.click()
                    else:
                        pass
                elif self.phase.getSubPhase().getName() == "Move":
                    self.addEvent(moveevent.MoveEvent(200, self.getActiveHero().getTile(), self.getActiveHero().getMovementRange()))
                    if event.type == MOUSEBUTTONUP and event.button == 1:
                        for x in self.getTilesWithRange(self.getActiveHero().getMovementRange(), self.getActiveHero().getTile()):
                             if x.collidepoint(event.pos) and not self.cancelButton.collidepoint(event.pos) and not self.backButton.collidepoint(event.pos):
                                self.processMove(x)
                        choice = self.choiceBox.collidepoint(event.pos)
                        if choice:
                            choice.click()
                elif self.phase.getSubPhase().getName() == "Attack":
                    if event.type == MOUSEBUTTONUP:
                        choice = self.choiceBox.collidepoint(event.pos)
                        if choice:
                            choice.click()
                elif self.phase.getSubPhase().getName() == "Melee":
                    self.addEvent(targetevent.TargetEvent(2, self.getActiveHero().getTile(), 2, (255,0,0)))
                    if event.type == MOUSEBUTTONUP and event.button == 1:

                        for x in self.getEvent(2).getTiles():
                             if x.collidepoint(event.pos) and x.getGameObject() != None or (x.getGameObject() != None and x.getGameObject().collidepoint(event.pos)):
                                self.processMeleeAttack(self.getActiveHero(), x.getGameObject())
                                self.hexBoard.setDirection(self.getActiveHero(), x.getCenter())
                        choice = self.choiceBox.collidepoint(event.pos)
                        if choice:
                            choice.click()
                elif self.phase.getSubPhase().getName() == "Ranged":
                    self.addEvent(targetevent.TargetEvent(2, self.getActiveHero().getTile(),self.getActiveHero().getRangedRange(), (255,0,0)))

                    if event.type == MOUSEBUTTONUP and event.button == 1:

                        for x in self.getEvent(2).getTiles():
                            if x.collidepoint(event.pos) and x.getGameObject() != None or (x.getGameObject() != None and x.getGameObject().collidepoint(event.pos)):
                                self.processRangedAttack(self.getActiveHero(), x.getGameObject())
                                self.hexBoard.setDirection(self.getActiveHero(), x.getCenter())
                        choice = self.choiceBox.collidepoint(event.pos)
                        if choice:
                            choice.click()
                elif self.phase.getSubPhase().getName() == "Spell":
                    if event.type == MOUSEBUTTONUP:
                        choice = self.choiceBox.collidepoint(event.pos)
                        if choice:
                            choice.click()
                elif self.phase.getSubPhase().getName() == "EndTurn":
                    if event.type == MOUSEMOTION:
                        self.hexBoard.setDirection(self.getActiveHero(), event.pos)
                    if event.type == MOUSEBUTTONUP and event.button == 1:
                        self.chooseDirection(event.pos)
                        self.startPhase()
                elif self.phase.getSubPhase().getName() == "TargetSpell":
                    self.addEvent(targetevent.TargetEvent(3, self.getActiveHero().getTile(), self.currentSpell.getRange(), (255,0,0)))
                    if event.type == MOUSEBUTTONUP and event.button == 1:
                        for x in self.getEvent(3).getTiles():
                            if (x.collidepoint(event.pos) or (x.getGameObject() != None and x.getGameObject().collidepoint(event.pos))) and x.getGameObject() != None:
                                self.currentSpell.target(x.getGameObject())
                                xpos = x.getCenter()[0]
                                ypos = x.getCenter()[1]
                                ypos -= 25
                                xpos -= 10
                                self.emitter = self.currentSpell.getParticleEmitter((xpos, ypos))
                                self.attacked = True
                                self.startPhase()
                                self.animations.append(textanimation.TextAnimation("Spell: {} applied!".format(self.currentSpell.name), x.getCenter(), (0,0,0), 150, 24))
                        choice = self.choiceBox.collidepoint(event.pos)
                        if choice:
                            choice.click()
                if self.checkForWinner():
                    self.activeHero = self.order[0]
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
        dmg = attacker.rangedAttack(defender)
        self.attacked = True
        self.isDead(defender)
        self.startPhase()
        if dmg != None or str(dmg) == '0':
            self.animations.append(textanimation.TextAnimation(str(dmg) + " Damage!", defender.getTile().getCenter()))
        elif dmg == None:
            self.animations.append(textanimation.TextAnimation("Dodged!", defender.getTile().getCenter()))
    def processMeleeAttack(self, attacker, defender):
        dmg = attacker.meleeAttack(defender)
        self.attacked = True
        self.isDead(defender)
        self.startPhase()
        if dmg != None or str(dmg) == '0':
            self.animations.append(textanimation.TextAnimation(str(dmg) + " Damage!", defender.getTile().getCenter()))
        elif dmg == None:
            self.animations.append(textanimation.TextAnimation("Dodged!", defender.getTile().getCenter()))
    def getActiveHero(self):
        return self.order[self.phaseCount]
    def update(self):

        self.syncBoard()
        if self.emitter and not self.emitter.dead:
            self.emitter.update()
        else:
            self.emitter = None
        if self.phase.getSubPhase().getName() == "TurnStart" and self.partyManager.checkHero(self.getActiveHero()) != 1:
            self.processAITurn(*self.ai.processTurn(self.hexBoard, self.getActiveHero(), self.moved, self.attacked))
        self.checkForWinner()
        if self.p1Dead:
            self.ismain = False
        if self.p2Dead:
            self.ismain = False
        self.updateBackground()
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
        currtime = time.clock()
        if currtime - self.lastTime > .2:
            self.battleStatsI += 1
            self.lastTime = currtime
            if self.battleStatsI > 5:
                self.battleStatsI = 0
        h = self.getActiveHero()
        if self.mouseOver != None:
            print "getting here"
            b = herobattlestats.HeroBattleStats(self.mouseOver, 0, self.surface.get_rect().height - 100)
        else:
            b = herobattlestats.HeroBattleStats(h, 0, self.surface.get_rect().height - 100)
        b.draw(surface, self.battleStatsI)
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
    def populateBackground(self):
        while len(self.clouds) < 15:
            self.clouds.append(cloud.Cloud(pygame.image.load("images/cloud{}.png".format(random.randrange(1,9))), (random.randrange(0, self.surface.get_rect().width), random.randrange(0, self.surface.get_rect().height)), random.randrange(1,4)))
    def updateBackground(self):
        tempclouds = []
        for x in self.clouds:
            x.update()
            if x.x < self.surface.get_rect().width:
                tempclouds.append(x)
        self.clouds = tempclouds
        if len(self.clouds) < 20:
            self.clouds.append(cloud.Cloud(pygame.image.load("images/cloud{}.png".format(random.randrange(1,9))), (-200, random.randrange(0, self.surface.get_rect().height - 50)), random.randrange(2,4)))
    def drawBackground(self, surface):
        for x in self.clouds:
            x.draw(surface)
    def draw(self, surface):
        surface.fill((0,104,139))
        self.drawBackground(surface)
        self.backButton.setRect(pygame.Rect(self.surface.get_rect().width - 100,0,100,50))
        
        self.hexBoard.drawTiles(surface)
        for x in self.events:
            if x.getID() < 100:
                x.draw(surface)
        for x in self.events:
            if x.getID() > 100:
                x.draw(surface)
        self.hexBoard.drawHeroes(surface)
        if self.phase.getName() == "Main":
            if self.phase.getSubPhase().getName() != "TurnStart":
                pass
                #self.cancelButton.draw(surface)
            if self.phase.getSubPhase().getName() == "TurnStart":
                self.choiceBox.draw(surface)
            if self.phase.getSubPhase().getName() == "Attack" or self.phase.getSubPhase().getName() == "Spell" or self.phase.getSubPhase().getName() == "TargetSpell" or self.phase.getSubPhase().getName() == "Move" or self.phase.getSubPhase().getName() == "Melee" or self.phase.getSubPhase().getName() == "Ranged":
                self.choiceBox.draw(surface)
            if self.phase.getSubPhase().getName() == "Animation" and self.heroAnimation != None and self.heroAnimation.working == True:
                if self.getActiveHero().getTile() != None:
                    self.getActiveHero().draw(surface, True)
                node = self.heroAnimation.animate(surface)
                if node != None:
                    print node.getID()
                    for x in range(len(self.hexBoard.tiles)):
                        for y in range(len(self.hexBoard.tiles[x])):
                            if self.hexBoard.tiles[x][y].getID() == node.getID():
                                self.getActiveHero().moving = False
                                self.hexBoard.tiles[x][y].setGameObject(self.getActiveHero())
                                self.hexBoard.tiles[x][y].getGameObject().draw(surface)
                                self.getActiveHero().moving = True
                                self.heroAnimation = None
                                self.startPhase()
            #self.endTurnButton.draw(surface)

        for x in self.animations:
            if not x.animate(surface):
                self.animations.remove(x)
        if not self.checkForWinner():
            self.drawActiveHero(surface)
        self.backButton.draw(surface)
        if self.emitter:
            self.emitter.draw(surface)

if __name__ == "__main__":
    pygame.init()
    b = BattleScene(pygame.display.set_mode((800,600)))
