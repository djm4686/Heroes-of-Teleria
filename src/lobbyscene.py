import pygame, networking, player, socket, ast, button, lobby, party, time, networkedbattlescene, hero
from pygame.locals import *
class LobbyScene:
    def __init__(self, surface, player, party = party.AI):
        pygame.init()
        self.party = party
        self.surface = surface
        self.player = player
        self.ismain = True
        self.lobbies = []
        self.createLobbyButton = button.Button(self.makeText("Create Lobby"), self.createLobby)
        self.refreshButton = button.Button(self.makeText("Refresh"), self.getLobbies)
        self.backButton = button.Button(self.makeText("Back"), self.back)
        self.backButton.setRect(pygame.Rect(600, 500, 200,100))
        self.searchingTextI = 0
        self.cancelSearchButton = button.Button(self.makeText("Cancel"), self.cancelSearch)
        self.cancelSearchButton.setRect(pygame.Rect(0,0,100,50))
        self.cancelSearchButton.setCenter(self.surface.get_rect().center)
        self.refreshButton.setRect(pygame.Rect(600, 100, 200,100))
        self.createLobbyButton.setRect(pygame.Rect(600, 0, 200,100))
        self.getLobbies()
        self.mainLoop()
    def back(self):
        self.ismain = False
    def createGame(self, ide, player1, player2, rows=16, cols=8):
        HOST, PORT = "localhost", 9999
        data = networking.DataFrame(networking.Header(1, "createMatch"), {"gameID" : ide, "player1" : str(player1), "player2" : str(player2), "rows" : str(rows), "cols" : str(cols)}).toString()

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
        if received["header"]["reqtype"] == "success":
            pass
            self.error = False
        else:
            self.error = True
    def challenge(self, ide):
        HOST, PORT = "localhost", 9999
        data = networking.DataFrame(networking.Header(1, "challenge"), {"id" : self.player.getID(), "lobby" : ide}).toString()

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
            p = party.Party(self.player)
            for h in received["data"]["heroes"]:
                
                p.addHero(hero.createFromJSON(ast.literal_eval(h)))
            print self.player.getID()
            self.createGame(ide, received["data"]["playerID"], self.player.getID())
            b = networkedbattlescene.NetworkedBattleScene(ide, self.surface, self.player, self.party, p)
            self.error = False
        else:
            self.error = True
    def deleteLobby(self):
        HOST, PORT = "localhost", 9999
        data = networking.DataFrame(networking.Header(1, "deleteLobby"), {"id" : self.player.getID()}).toString()

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
    def connectToGame(self, ide):
        HOST, PORT = "localhost", 9999
        data = networking.DataFrame(networking.Header(1, "connectToGame"), {"playerID" : ide}).toString()

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
        print received
        received = ast.literal_eval(received)
        if received["header"]["reqtype"] == "success":
            p = party.Party(self.player)
            for h in received["data"]["heroes"]:
                
                p.addHero(hero.createFromJSON(ast.literal_eval(h)))
            b = networkedbattlescene.NetworkedBattleScene(received["data"]["gameID"], self.surface, self.player, self.party, p)

            return 1
        else:
            return 0
        
    def lobbyKeepAlive(self):
        lastTime = time.clock()
        lastTimeDots = time.clock()
        alive = True
        self.makeSearchingText()
        while alive:
            self.cancelSearchButton.draw(self.surface)
            pygame.draw.rect(self.surface, (128,128,128), self.searchingTextRect)
            self.surface.blit(self.searchingText, self.searchingTextRect)
            pygame.display.update()
            currtime = time.clock()
            if currtime - lastTime > 5:
                if self.lobbyCheckForChallenge():
                    alive = False
                    self.connectToGame(self.player.getID())
                lastTime = currtime
            if currtime - lastTimeDots > .5:
                self.makeSearchingText()
                lastTimeDots = currtime
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.deleteLobby()
                    pygame.quit()
                if event.type == MOUSEBUTTONDOWN and self.cancelSearchButton.collidepoint(event.pos):
                    alive = self.cancelSearchButton.callBack()
    def makeSearchingText(self):
            text = "Waiting For Opponent"
            for _ in range(self.searchingTextI):
                text += "."
            if self.searchingTextI > 3:
                self.searchingTextI = 0
            else:
                self.searchingTextI += 1
            self.searchingText = self.makeText(text)
            self.searchingTextRect = pygame.Rect(0,0,200,50)
            self.searchingTextRect.center = self.surface.get_rect().center
            self.searchingTextRect.y -= 50
            self.searchingTextRect.x += 35
    def cancelSearch(self):
        self.deleteLobby()
        return False
    def lobbyCheckForChallenge(self):
        HOST, PORT = "localhost", 9999
        data = networking.DataFrame(networking.Header(1, "checkForChallenge"), {"id" : self.player.getID()}).toString()

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
        if received["header"]["reqtype"] == "playerFound":
            return 1
        else:
            return 0
    def createLobby(self):
        HOST, PORT = "localhost", 9999
        data = networking.DataFrame(networking.Header(1, "createLobby"), {"id" : self.player.getID()}).toString()

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
            self.lobbyKeepAlive()
        else:
            self.error = True
    def update(self):
        pass
    def makeText(self, text):
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
        return self.font.render(text, True, (0,0,0))
    def getLobbies(self):
        HOST, PORT = "localhost", 9999
        data = networking.DataFrame(networking.Header(1, "fetchLobbies")).toString()

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
        self.lobbies = []
        if received["header"]["reqtype"] == "sendLobbies":
            i = 0
            for x in received["data"]["lobbies"]:
                x = ast.literal_eval(x)
                l = lobby.Lobby(x["id"], x["name"], self.challenge, x["id"])
                l.setRect(pygame.Rect(0, i * 100, 600, 100))
                self.lobbies.append(l)
                i += 1
            self.error = False
        else:
            self.error = True
    def mainLoop(self):
        while self.ismain:
            self.eventLoop()
            self.update()
            pygame.display.update()
            self.draw(self.surface)
    def eventLoop(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if self.createLobbyButton.collidepoint(event.pos):
                    self.createLobby()
                if self.backButton.collidepoint(event.pos):
                    self.backButton.callBack()
                if self.refreshButton.collidepoint(event.pos):
                    self.refreshButton.callBack()
                for x in self.lobbies:
                    if x.collidepoint(event.pos):
                        x.Button.callBack()
    def draw(self, surface):
        surface.fill((128,128,128))
        self.createLobbyButton.draw(surface)
        self.refreshButton.draw(surface)
        self.backButton.draw(surface)
        for x in self.lobbies:
            x.draw(surface)
