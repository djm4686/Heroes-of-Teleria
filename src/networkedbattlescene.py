import battlescene, socket, ast, networking
import pygame, party, sys, button, activeHeroEvent, targetevent, battlepartymanager, zoneevent, random, imageevent, herostatusevent, phase, herobattlestats, moveevent
from pygame.locals import *
class NetworkedBattleScene(battlescene.BattleScene):
    def __init__(self, ide, surface, player, party1=party.AI, party2=party.AI2):
        self.ide = ide
        self.player = player
        battlescene.BattleScene.__init__(self, surface, party1=party2, party2=party1, ai= False)
        
    def isItMyTurn(self, hero):
        if hero.getPlayerID() == self.player.getID():
            return True
        else:
            return False
    def askServerForBoard(self):
        pass
    def sendTileChoice(self, row, col):
        HOST, PORT = "localhost", 9999
        data = networking.DataFrame(networking.Header(1, "sendTileChoice"), {"gameID" : self.ide, "id" : self.player.getID(), "col" : col, "row" : row, "hero" : self.order[self.phaseCount].getID()}).toString()

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
            return 1
        else:
            return 0
    def eventLoop(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
            if event.type == MOUSEMOTION and self.moving == True:
                self.hexBoard.setNewCoords((event.pos[0] - self.originp[0], event.pos[1] - self.originp[1]))
                self.originp = event.pos
            if event.type == MOUSEBUTTONDOWN and event.button == 3:
                self.moving = True
                self.originp = event.pos
            if event.type == MOUSEBUTTONUP and event.button == 3:
                self.moving = False
            if event.type == MOUSEBUTTONUP and event.button == 1 and self.backButton.getRect().collidepoint(event.pos):
                self.ismain = False
            if self.phase.getName() == "Placement":
                if self.phase.getSubPhase().getName() == "Direction":
                    self.addEvent(activeHeroEvent.activeHeroEvent(0, self.order[self.phaseCount].getTile()))
                    if event.type == MOUSEMOTION:
                        self.hexBoard.setDirection(self.order[self.phaseCount], event.pos)
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        self.hexBoard.setDirection(self.order[self.phaseCount], event.pos)
                        self.phase.addSubPhase(phase.Phase("Placement"))
                        self.phaseCount = self.phaseCount + 1
                        if self.phaseCount >= len(self.order):
                                self.resetPhase()
                                self.phase = phase.Phase("Main")
                                self.phase.addSubPhase(phase.Phase("TurnStart"))
                elif self.phase.getSubPhase().getName() == "Placement":
                    if not self.isItMyTurn(self.order[self.phaseCount]) and self.ai == True:
                        ts = self.hexBoard.getZone2()
                        r = ts[random.randrange(0, len(ts))]
                        while r.getGameObject() != None:
                            r = ts[random.randrange(0, len(ts))]
                        activeTile = r
                        activeTile.setGameObject(self.order[self.phaseCount])
                        self.phaseCount = self.phaseCount + 1
                        if self.phaseCount >= len(self.order):
                                self.resetPhase()
                                self.phase = phase.Phase("Main")
                                self.phase.addSubPhase(phase.Phase("TurnStart"))
                    elif not self.isItMyTurn(self.order[self.phaseCount]) and self.ai == False:
                        self.events = []
                    if self.isItMyTurn(self.order[self.phaseCount]):
                        self.addEvent(zoneevent.ZoneEvent(1,self.hexBoard.getZone1()))
                    activeTile = None
                    if event.type == MOUSEMOTION:
                        activeTile = self.hexBoard.collidepoint(event.pos)
                        
                        if activeTile != None and activeTile.getZone() == self.partyManager.checkHero(self.order[self.phaseCount]):
                            self.addEvent(activeHeroEvent.activeHeroEvent(0, activeTile))
                            self.addEvent(imageevent.ImageEvent(2, self.order[self.phaseCount].getActiveHeroClass().getSprite(), activeTile))
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        activeTile = self.hexBoard.collidepoint(event.pos)
                        if activeTile != None and activeTile.getGameObject() == None and activeTile.getZone() == self.partyManager.checkHero(self.order[self.phaseCount]):
                            activeTile.setGameObject(self.order[self.phaseCount])
                            x, y = self.hexBoard.getTileIndeces(activeTile)
                            self.sendTileChoice(x, y)
                            self.phase.addSubPhase(phase.Phase("Direction"))
                            if self.phaseCount >= len(self.order):
                                self.resetPhase()
                                self.phase = phase.Phase("Main")
                                self.phase.addSubPhase(phase.Phase("TurnStart"))
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
                    if self.partyManager.checkHero(self.order[self.phaseCount]) == 1:
                        self.playerTurn = True
                        for x in self.choiceButtons:
                            if event.type == MOUSEBUTTONUP and x.collidepoint(event.pos):
                                x.callBack()
                    else:
                        self.nextHero()
                elif self.phase.getSubPhase().getName() == "Move":
                    self.addEvent(moveevent.MoveEvent(2, self.order[self.phaseCount].getTile(), self.order[self.phaseCount].getMovementRange()))
                    for x in self.getTilesWithRange(self.order[self.phaseCount].getMovementRange(), self.order[self.phaseCount].getTile()):
                        if event.type == MOUSEBUTTONUP and event.button == 1 and x.collidepoint(event.pos) and not self.cancelButton.collidepoint(event.pos) and not self.backButton.collidepoint(event.pos):
                            x.setGameObject(self.order[self.phaseCount])
                            self.startPhase()
                            self.moved = True
                elif self.phase.getSubPhase().getName() == "Attack":
                    for x in self.choiceButtons:
                        if event.type == MOUSEBUTTONUP and x.collidepoint(event.pos):
                            x.callBack()
                elif self.phase.getSubPhase().getName() == "Melee":
                    self.addEvent(targetevent.TargetEvent(2, self.order[self.phaseCount].getTile(), 2, (255,0,0)))
                    for x in self.getEvent(2).getTiles():
                        if event.type == MOUSEBUTTONUP and event.button == 1 and x.collidepoint(event.pos) and x.getGameObject() != None:
                            attacker = self.order[self.phaseCount]
                            defender = x.getGameObject()
                            attacker.meleeAttack(defender)
                            self.attacked = True
                            self.isDead(defender)
                            self.startPhase()
                elif self.phase.getSubPhase().getName() == "Ranged":
                    self.addEvent(targetevent.TargetEvent(2, self.order[self.phaseCount].getTile(),self.order[self.phaseCount].getRangedRange(), (255,0,0)))
                    for x in self.getEvent(2).getTiles():
                        if event.type == MOUSEBUTTONUP and event.button == 1 and x.collidepoint(event.pos) and x.getGameObject() != None:
                            attacker = self.order[self.phaseCount]
                            defender = x.getGameObject()
                            attacker.rangedAttack(defender)
                            self.attacked = True
                            self.isDead(defender)
                            self.startPhase()
                if self.phase.getSubPhase().getName() != "TurnStart":
                    if event.type == MOUSEBUTTONUP and self.cancelButton.collidepoint(event.pos):
                        self.cancelButton.callBack()
                self.addEvent(activeHeroEvent.activeHeroEvent(0, self.order[self.phaseCount].getTile()))
            elif self.phase.getName() == "test":
                if event.type == MOUSEMOTION:
                    tile = self.hexBoard.collidepoint(event.pos)
                    if tile != None:
                        self.addEvent(targetevent.TargetEvent(tile, 2))
