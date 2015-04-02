import pygame, button
class Lobby:
    def __init__(self, ide, playername, callback = None, cbp = []):
        pygame.init()
        self.callback = callback
        self.id = ide
        self.font = pygame.font.Font(pygame.font.get_default_font(), 28)
        self.name = playername
        self.rect = pygame.Rect(0,0,100,100)
        self.Button = button.Button(self.font.render(self.name + "'s game! - Avg Hero Level: 1", True, (0,0,0)), self.callback, cbp)
    def setRect(self, rect):
        self.Button.setRect(rect)
    def collidepoint(self, point):
        return self.Button.collidepoint(point)
    def toString(self):
        return "{\"id\" : \"" + str(self.id) + "\", \"name\" : \"" + self.name + "\"}"
    def draw(self, surface):
        self.Button.draw(surface)
