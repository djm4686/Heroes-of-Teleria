import pygame, random
BLACK = (0,0,0)
class IsometricTile:
    def __init__(self, ide, x, y, size = 50, height = 1, xindex=0, yindex=0, zone = 1, spritePath = "images/map/Grass_rect_png2.png"):
        self.x = x
        self.y = y
        self.id = ide
        self.height = height
        self.size = size
        self.width = size
        self.xindex = xindex
        self.yindex = yindex
        self.gameObject = None
        self.n1 = None
        self.n2 = None
        self.n3 = None
        self.n4 = None
        self.selected = False
        self.spritePath = spritePath
        self.sprite = pygame.image.load(self.spritePath)
        self.zone = zone
        self.points = [(self.x, self.y - ((self.height - 1)*16)),
                       (self.x + int(self.width * .5), self.y + int(self.width * .5 * .5)- ((self.height - 1)*16)),
                       (self.x, self.y + int(self.width * .5)- ((self.height - 1)*16)),
                       (self.x - int(self.width * .5), self.y + int(self.width * .5 * .5)- ((self.height - 1)*16)),
                       (self.x, self.y- ((self.height - 1)*16))]
    @staticmethod
    def makeFromJSON(json):
        id = json["tileID"]
        x = json["x"]
        y = json["y"]
        height = json["height"]
        n1ID = json["n1"]
        n2ID = json["n2"]
        n3ID = json["n3"]
        n4ID = json["n4"]
        spritePath = json["sprite"]
        xindex = json["xindex"]
        yindex = json["yindex"]
        size = json["size"]
        zone = json["zone"]
        return IsometricTile(id, x, y, size, height, xindex, yindex, zone, spritePath)

    def changeSprite(self, path):
        self.spritePath = path
        self.sprite = pygame.image.load(self.spritePath)

    def changeHeight(self, h):
        self.height = h
        self.reMakePoints()
    def generateJSON(self):
        json = "'tileID': {}, 'x': {}, 'y': {}, 'height': {}, 'n1': {}, 'n2': {}, 'n3': {}, 'n4': {}, 'sprite': '{}', 'xindex': {}, 'yindex': {}, 'size': {}, 'zone': {}"
        json = json.format(self.id,
                            self.x,
                            self.y,
                            self.height,
                            self.n1.getID() if self.n1 else None,
                            self.n2.getID() if self.n2 else None,
                            self.n3.getID() if self.n3 else None,
                            self.n4.getID() if self.n4 else None,
                            self.spritePath,
                            self.xindex,
                            self.yindex,
                            self.size,
                            self.zone)
        return json

    def getID(self):
        return self.id
    def reMakePoints(self):
        self.points = [(self.x, self.y- ((self.height - 1)*16)),
                       (self.x + int(self.width * .5), self.y + int(self.width * .5 * .5)- ((self.height - 1)*16)),
                       (self.x, self.y + int(self.width * .5)- ((self.height - 1)*16)),
                       (self.x - int(self.width * .5), self.y + int(self.width * .5 * .5)- ((self.height - 1)*16)),
                       (self.x, self.y- ((self.height - 1)*16))]
    def getZone(self):
        return self.zone
    def getCoords(self):
        return self.x,self.y
    def getCenter(self):
        return int(self.x), int(self.y + (self.width *.5 * .5)- ((self.height - 1)*16))
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
    def select(self):
        self.selected = True
    def drawShaded(self, surface, color):
        pygame.draw.polygon(surface, color, self.points)
    def drawOutline(self, surface, color, width):
        pygame.draw.lines(surface, color, False, self.points, width)
    def collidepoint(self, point):
        x, y = point
        if y > (-.5 * x) + (self.y - ((self.height - 1)*16) - (-.5 * self.x)) and y > (.5 * x) + (self.y - ((self.height - 1)*16)- (.5 * self.x)) and y < (.5 * x) + ((self.y - ((self.height - 1)*16)+ (self.size * .5)) - (.5 * self.x)) and y < (-.5 * x) + ((self.y - ((self.height - 1)*16) + (self.size * .5)) - (-.5 * self.x)):
            return True
        else:
            return False
    def drawHero(self, surface):
        if self.gameObject != None:
            self.gameObject.draw(surface)
    def drawTile(self, surface):
        for x in range(self.height):
            surface.blit(self.sprite, pygame.Rect(self.x-(.5 * self.size), self.y - (x * 16), self.size, self.size * .5))
        pygame.draw.lines(surface, BLACK, True, self.points, 2)
        

