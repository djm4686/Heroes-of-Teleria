import pygame
BLACK = (0,0,0)
class IsometricTile:
    def __init__(self, ide, x, y, size = 50, zone = 1):
        self.x = x
        self.y = y
        self.id = ide
        self.size = size
        self.width = size
        self.gameObject = None
        self.n1 = None
        self.n2 = None
        self.n3 = None
        self.n4 = None
        self.sprite = pygame.image.load("images/Grass_png.png")
        self.zone = zone
        self.points = [(self.x, self.y),
                       (self.x + int(self.width * .5), self.y + int(self.width * .5 * .5)),
                       (self.x, self.y + int(self.width * .5)),
                       (self.x - int(self.width * .5), self.y + int(self.width * .5 * .5)),
                       (self.x, self.y)]
        
    def getID(self):
        return self.id
    def reMakePoints(self):
        self.points = [(self.x, self.y),
                       (self.x + int(self.width * .5), self.y + int(self.width * .5 * .5)),
                       (self.x, self.y + int(self.width * .5)),
                       (self.x - int(self.width * .5), self.y + int(self.width * .5 * .5)),
                       (self.x, self.y)]
    def getZone(self):
        return self.zone
    def getCoords(self):
        return self.x,self.y
    def getCenter(self):
        return int(self.x), int(self.y + (self.width *.5 * .5))
    def setGameObject(self, g):
        self.gameObject = g
        if g.tile == None:
            g.setTile(self)
    def getGameObject(self):
        return self.gameObject
    def getNeighbors(self):
        return [self.n1, self.n2, self.n3, self.n4]
    def getN1(self):
        return self.n1
    def setN1(self, n):
        self.n1 = n
    def getN2(self):
        return self.n2
    def setN2(self, n):
        self.n2 = n
    def getN3(self):
        return self.n3
    def setN3(self, n):
        self.n3 = n
    def getN4(self):
        return self.n4
    def setN4(self, n):
        self.n4 = n
    def drawShaded(self, surface, color):
        pygame.draw.polygon(surface, color, self.points)
    def drawOutline(self, surface, color, width):
        pygame.draw.lines(surface, color, False, self.points, width + 2)
    def collidepoint(self, point):
        x, y = point
        if y > (-.5 * x) + (self.y - (-.5 * self.x)) and y > (.5 * x) + (self.y - (.5 * self.x)) and y < (.5 * x) + ((self.y + (self.size * .5)) - (.5 * self.x)) and y < (-.5 * x) + ((self.y + (self.size * .5)) - (-.5 * self.x)):
            return True
        else:
            return False
    def drawHero(self, surface):
        if self.gameObject != None:
            self.gameObject.draw(surface)
    def drawTile(self, surface):
        
        surface.blit(self.sprite, pygame.Rect(self.x-(.5 * self.size), self.y, self.size, self.size * .5))
        pygame.draw.lines(surface, BLACK, True, self.points, 2)
        

