import pygame, button, herocreationscreen, particles, phase, socket, networking, ast, player, lobbyscene, networkedpartyscene
from pygame.locals import *
class TitleScene:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((800,600))
        self.nameLabel = pygame.image.load("images/name.png")
        self.nameRect = pygame.Rect(0,0, self.nameLabel.get_rect().width, self.nameLabel.get_rect().height)
        self.nameRect.center = self.surface.get_rect().center
        self.nameRect.y = self.nameRect.y - 100
        self.phase = phase.Phase("Main")
        self.usernameButton = button.Button(self.makeText("Username", 20, color = (255,255,255)), self.usernamePhase, color = (0,0,0), textColor = (255,255,255))
        self.passwordButton = button.Button(self.makeText("Password", 20, color = (255,255,255)), self.passwordPhase, color = (0,0,0), textColor = (255,255,255))
        temprect = pygame.Rect(self.nameRect.x, self.nameRect.y + 100,150,20)
        temprect.center = self.nameRect.center
        temprect.y = temprect.y + 100
        self.error = False
        self.usernameButton.setRect(pygame.Rect((temprect.x,temprect.y), (150,20)))
        self.passwordButton.setRect(pygame.Rect((temprect.x,temprect.y + 30), (150,20)))
        self.cancelButton = button.Button(self.makeText("Cancel", 20), self.mainPhase)
        self.registerButton = button.Button(self.makeText("Register", 20), self.register)
        self.loginButton = button.Button(self.makeText("Login", 20), self.login)
        self.lamp = pygame.image.load("images/lamp.png")
        self.multiplayerButton = button.Button(self.makeText("Multiplayer", 20), self.multiplayerPhase)
        self.startButton = button.Button(self.makeText("Play", 20), self.partyScreen)
        rect = pygame.Rect(self.nameRect.x, self.nameRect.y + 100,200,50)
        rect.center = self.nameRect.center
        rect.y = rect.y + 150
        self.startButton.setRect(pygame.Rect((rect.x,rect.y-50), (200,50)))
        rect.y = rect.y + 50
        self.multiplayerButton.setRect(pygame.Rect((rect.x,rect.y-50), (200,50)))
        self.loginButton.setRect(pygame.Rect((rect.x,rect.y), (200,50)))
        rect.y = rect.y + 50
        self.registerButton.setRect(pygame.Rect((rect.x,rect.y), (200,50)))
        rect.y = rect.y + 50
        self.cancelButton.setRect(pygame.Rect((rect.x,rect.y), (200,50)))
        self.leftLampRect = pygame.Rect(0,0,50,75)
        self.rightLampRect = pygame.Rect(0,0,50,75)
        self.leftLampRect.center = self.nameRect.center
        self.rightLampRect.center = self.nameRect.center
        self.leftLampRect.x = self.leftLampRect.x - 125
        self.rightLampRect.x = self.rightLampRect.x + 125
        self.leftLampRect.y = self.leftLampRect.y + 115
        self.rightLampRect.y = self.rightLampRect.y + 115
        self.spm1 = particles.SmokeParticleManager(self.leftLampRect.center[0], self.leftLampRect.y + 5)
        self.spm2 = particles.SmokeParticleManager(self.rightLampRect.center[0], self.rightLampRect.y + 5)
        self.userChars = ""
        self.passwordChars = ""
        self.mainLoop()

    def register(self):
        HOST, PORT = "localhost", 9999
        print self.passwordChars
        data = networking.DataFrame(networking.Header(1, "registerAccount"), {"name" : self.userChars, "password" : self.passwordChars}).toString()

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
            print "Success"
            self.error = False
        else:
            self.error = True
    def usernamePhase(self):
        self.phase = phase.Phase("Username")
    def passwordPhase(self):
        self.phase = phase.Phase("Password")
    def multiplayerPhase(self):
        self.phase = phase.Phase("Multiplayer")
    def mainPhase(self):
        self.phase = phase.Phase("Main")
    def login(self):
        HOST, PORT = "localhost", 9999
        data = networking.DataFrame(networking.Header(1, "login"), {"name" : self.userChars, "password" : self.passwordChars}).toString()

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
            n = networkedpartyscene.HeroCreationScreen(self.surface, player.Player(received["data"]["id"], received["data"]["username"]))
            self.error = False
        else:
            self.error = True
        
    def update(self):
        self.spm1.update()
        self.spm2.update()
    def partyScreen(self):
        p = herocreationscreen.HeroCreationScreen(self.surface)
    def makeText(self, text, size = 12, font = pygame.font.get_default_font(), color = (0,0,0)):
        self.font = pygame.font.Font(pygame.font.match_font(font), size)
        return self.font.render(text, True, color)
    def mainLoop(self):
        while True:
            self.eventLoop()
            self.update()
            self.draw(self.surface)
            pygame.display.update()
    def eventLoop(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if self.phase.getName() == "Main":
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if self.startButton.collidepoint(event.pos):
                        self.startButton.callBack()
                    if self.multiplayerButton.collidepoint(event.pos):
                        self.multiplayerButton.callBack()
            if self.phase.getName() == "Multiplayer":
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.usernameButton.collidepoint(event.pos):
                    self.usernameButton.callBack()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1 and self.passwordButton.collidepoint(event.pos):
                    self.passwordButton.callBack()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1 and self.cancelButton.collidepoint(event.pos):
                    self.cancelButton.callBack()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1 and self.loginButton.collidepoint(event.pos):
                    self.loginButton.callBack()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1 and self.registerButton.collidepoint(event.pos):
                    self.registerButton.callBack()
            elif self.phase.getName() == "Username":
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.passwordButton.collidepoint(event.pos):
                    self.passwordButton.callBack()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1 and self.cancelButton.collidepoint(event.pos):
                    self.cancelButton.callBack()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1 and self.loginButton.collidepoint(event.pos):
                    self.loginButton.callBack()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1 and self.registerButton.collidepoint(event.pos):
                    self.registerButton.callBack()
                self.usernameButton.setText(self.makeText(self.userChars + "_", 20, color = (255,255,255)))
                if event.type == KEYDOWN and ((event.key >= 97 and event.key <=K_z and len(self.userChars) < 15) or(event.key >= K_0 and event.key <= K_9)):
                    self.userChars += unichr(event.key)
                if event.type == KEYDOWN and event.key == K_BACKSPACE:
                    self.userChars = self.userChars[0:-1]
            elif self.phase.getName() == "Password":
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.usernameButton.collidepoint(event.pos):
                    self.usernameButton.callBack()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1 and self.cancelButton.collidepoint(event.pos):
                    self.cancelButton.callBack()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1 and self.loginButton.collidepoint(event.pos):
                    self.loginButton.callBack()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1 and self.registerButton.collidepoint(event.pos):
                    self.registerButton.callBack()
                self.passwordButton.setText(self.makeText("".join(["*" for x in range(len(self.passwordChars))]) + "_", 20, color = (255,255,255)))
                if event.type == KEYDOWN and ((event.key >= 97 and event.key <=K_z and len(self.passwordChars) < 15) or(event.key >= K_0 and event.key <= K_9)):
                    self.passwordChars += unichr(event.key)
                if event.type == KEYDOWN and event.key == K_BACKSPACE:
                    self.passwordChars = self.passwordChars[0:-1]
    def draw(self, surface):
        surface.fill((128, 128, 128))
        surface.blit(self.nameLabel, self.nameRect)
        self.spm1.draw(surface)
        self.spm2.draw(surface)
        surface.blit(self.lamp, self.leftLampRect)
        surface.blit(self.lamp, self.rightLampRect)
        if self.phase.getName() == "Multiplayer":
            self.usernameButton.draw(surface)
            self.passwordButton.draw(surface)
            self.loginButton.draw(surface)
            self.registerButton.draw(surface)
            self.cancelButton.draw(surface)
        elif self.phase.getName() == "Main":
            self.startButton.draw(surface)
            self.multiplayerButton.draw(surface)
        elif self.phase.getName() == "Username":
            self.usernameButton.draw(surface)
            self.passwordButton.draw(surface)
            self.loginButton.draw(surface)
            self.registerButton.draw(surface)
            self.cancelButton.draw(surface)
        elif self.phase.getName() == "Login":
            pass
        elif self.phase.getName() == "Password":
            self.usernameButton.draw(surface)
            self.passwordButton.draw(surface)
            self.cancelButton.draw(surface)
            self.registerButton.draw(surface)
            self.loginButton.draw(surface)
        if self.error == True:
            self.errorLabel = self.makeText("ERROR: Invalid login, or already registered", 30, color = (255,0,0))
            r = pygame.Rect(0,0,self.errorLabel.get_rect().width, self.errorLabel.get_rect().height)
            r.center = surface.get_rect().center
            r.y = 0
            surface.blit(self.errorLabel, r)
if __name__ == "__main__":
    
    t = TitleScene()
