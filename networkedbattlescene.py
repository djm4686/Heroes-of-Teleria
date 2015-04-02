

import battlescene, socket, ast, networking, battlepartymanager, time, pygame
import party, hero
class NetworkedBattleScene(battlescene.BattleScene):
    def __init__(self, ide, surface, localplayer, networkedplayer, party1=party.getAi(), party2=party.getAi()):
        self.ide = ide
        self.player = localplayer
        self.networkedplayer = networkedplayer
        self.party1 = party1
        self.DataFrameFactory = lambda header, data: networking.DataFrame(networking.Header(1, header), data).toString()
        self.sendHeroChoices()
        time.sleep(5)
        self.sendToServer(self.DataFrameFactory("connectToGame", {"gameID" : self.ide, "playerID" : self.player.getID()}))
        battlescene.BattleScene.__init__(self, surface, party1=party2, party2=party1,  ai = False)

    def determineInitiative(self):
        heroID = int(self.sendToServer(self.DataFrameFactory("getCurrentHeroTurn", {"gameID" : self.ide}))["heroID"])
        self.order = [hero.createFromJSON(ast.literal_eval(x)) for x in self.sendToServer(self.DataFrameFactory("getHeroesInOrder", {"gameID" : self.ide}))["heroes"]]
        for x in self.order:
            if x.getID() == heroID:
                self.activeHero = x

    def initVars(self):
        self.partyManager = battlepartymanager.BattlePartyManager(self.party1, self.party2, self.player.getID(), self.networkedplayer.getID())
        self.heroes = [hero.createFromJSON(ast.literal_eval(x)) for x in self.getHeroesInGame()]
    def isItMyTurn(self, hero):
        if hero.getPlayerID() == self.player.getID():
            return True
        else:
            return False
    def sendToServer(self, data):
        print data
        HOST, PORT = "localhost", 9999
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((HOST, PORT))
            sock.sendall(data + "\n")
            received = sock.recv(10000)
            print "recieved: {}".format(received)
        finally:
            sock.close()
        received = ast.literal_eval(received)
        if received["header"]["reqtype"] == "success":
            return received["data"]
        else:
            return 0
    def mainLoop(self):
        while self.ismain:
            self.eventLoop(self.player.getID(), self.networkedplayer.getID())
            self.update()
            self.draw(self.surface)
            pygame.display.update()
    def enemyTurn(self):
        curTime = time.clock()
    def getHeroByID(self, ID):
        for x in self.heroes:
            if x.getID() == ID:
                return x
    def getHeroesInGame(self):
        data = self.DataFrameFactory("getHeroesInGame", {"gameID" : self.ide})
        ret = self.sendToServer(data)["heroes"]
        print ret
        return ret
    def getHeroes(self):
        data = self.DataFrameFactory("getHeroes", {"gameID" : self.ide})
        return self.sendToServer(data)
    def askServerForBoard(self):
        data = networking.DataFrame(networking.Header(1, "askForBoard"), {"gameID" : self.ide})
        data = self.sendToServer(data)
        if data != 0 and len(self.heroes) != 0:
            for column, row, heroid in data:
                self.hexBoard[column][row].setGameObject(self.getHeroByID(heroid))
    def netUpdate(self):
        self.netUpdate()
        self.heroes = [hero.createFromJSON(x) for x in self.getHeroesInGame()]
        self.askServerForBoard()
    def nextHero(self):
        self.netUpdate()
        super(NetworkedBattleScene, self).nextHero()
        data = self.DataFrameFactory("nextHero", {"gameID":self.ide, "turn": self.phaseCount})
        self.sendToServer(data)
    def chooseTile(self, activeTile):
        self.sendTileChoice(activeTile.xindex, activeTile.yindex)
        super(NetworkedBattleScene, self).chooseTile(activeTile)
    def sendTileChoice(self, row, col):
        data = self.DataFrameFactory("sendTileChoice", {"gameID" : self.ide, "id" : self.player.getID(), "col" : col, "row" : row, "hero" : self.order[self.phaseCount].getID()})
        self.sendToServer(data)
    def processMove(self, tile):
        data = self.DataFrameFactory("processMoveOrder", {"gameID": self.ide, "hero" : self.order[self.phaseCount].getID(), "tilex" : tile.xindex, "tiley" : tile.yindex})
        self.sendToServer(data)
        super(NetworkedBattleScene, self).processMove(tile)
    def processMeleeAttack(self, attacker, defender):
        data = self.DataFrameFactory("processMeleeAttack", {"gameID" : self.ide, "attacker" : attacker.getID(), "defender" : defender.getID()})
        self.sendToServer(data)
        super(NetworkedBattleScene, self).processMeleeAttack(attacker, defender)
    def processRangedAttack(self, attacker, defender):
        data = self.DataFrameFactory("processRangedAttack", {"gameID" : self.ide, "attacker" : attacker.getID(), "defender" : defender.getID()})
        self.sendToServer(data)
        super(NetworkedBattleScene, self).processRangedAttack(attacker, defender)
    def chooseDirection(self, pos):
        super(NetworkedBattleScene, self).chooseDirection(pos)
    def sendHeroChoices(self):
        data = self.DataFrameFactory("sendParty", {"gameID" : self.ide, "playerID" : self.player.getID(), "heroes" : [x.getID() for x in self.party1.getHeroes()]})
        self.sendToServer(data)