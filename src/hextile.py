import pygame as pg
from pygame.locals import *
import math
BLACK = (0,0,0)
class HexTile:
    def __init__(self, ide, x = 0, y = 0, size = 50, zone = 1):
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
        self.n5 = None
        self.n6 = None
        self.zone = zone
        self.points = [(self.x, self.y),
                       (self.x + .25 * self.size, self.y - .5 * self.size),
                       (self.x + .75 * self.size, self.y - .5 * self.size),
                       (self.x + self.size, self.y),
                       (self.x + .75 * self.size, self.y + .5 * self.size),
                       (self.x + .25 * self.size, self.y + .5 * self.size),
                       (self.x, self.y)]
    def getID(self):
        return self.id
    def reMakePoints(self):
        self.points = [(self.x, self.y),
                       (self.x + .25 * self.size, self.y - .5 * self.size),
                       (self.x + .75 * self.size, self.y - .5 * self.size),
                       (self.x + self.size, self.y),
                       (self.x + .75 * self.size, self.y + .5 * self.size),
                       (self.x + .25 * self.size, self.y + .5 * self.size),
                       (self.x, self.y)]
    def getZone(self):
        return self.zone
    def getCoords(self):
        return self.x,self.y
    def getCenter(self):
        return int(self.x + self.width * .5), self.y
    def setGameObject(self, g):
        if g.getTile() != None:
            g.getTile().gameObject = None
        self.gameObject = g
        self.gameObject.setTile(self)
    def getGameObject(self):
        return self.gameObject
    def getNeighbors(self):
        return [self.n1, self.n2, self.n3, self.n4, self.n5, self.n6]
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
    def getN5(self):
        return self.n5
    def setN5(self, n):
        self.n5 = n
    def getN6(self):
        return self.n6
    def setN6(self, n):
        self.n6 = n
    def collidepoint(self, point):
        x, y = point
##        slope1 = (self.y-self.y -(.5*self.size))/(self.x - self.x + (.25 * self.size))
##        slope2 = ((self.y - (.5 * self.size))-(self.y -(.5*self.size)))/((self.x + (.25 * self.size)) - self.x + (.25 * self.size))
##        slope3 = ((self.y - (.5 * self.size)) - self.y)/((self.x + (.75 * self.size)) - (self.x + self.size))
##        slope4 = (self.y - (self.y + .5 * self.size))/((self.x + self.size)-(self.x + (.75 * self.size)))
##        slope5 = ((self.y + (.5 * self.size))-(self.y + (.5 * self.size)))/((self.x + (.75 * self.size))-(self.x + (.25 * self.size)))
##        slope6 = ((self.y + (.5 * self.size))-self.y)/((self.x + (.25 * self.size)) - self.x)
##        b1 = -((slope1 * self.x) + self.y)
##        b2 = -((slope2 * (self.x + (.25 * self.size))) + (self.y - (.5 * self.size)))
##        b3 = -((slope3 * (self.x + (.75 * self.size))) + (self.y - (.5 * self.size)))
##        b4 = -((slope4 * (self.x + self.size)) + (self.y))
##        b5 = -((slope5 * (self.x + (.75 * self.size))) + (self.y + (.5 * self.size)))
##        b6 = -((slope6 * self.x) + self.y)
        if x > self.x and x < (self.x + self.width) and y > (self.y - (self.width * .5)) and y < (self.y + (self.width * .5)) and y > (-2 * x) + (math.ceil((math.tan(math.radians(63))) * self.x) + self.y) and y < (-2 * x) + (math.ceil((math.tan(math.radians(63))) * (self.x + (self.width * .75)) + (self.y+(self.width*.5)))) and y < (2 * x) + (self.y - (2 * self.x)) and y > (2 * x) + ((self.y - (self.width*.5)) - (2 * (self.x + (self.width*.75)))):
            return True
        else:
            return False
    def drawShaded(self, surface, color):
        pg.draw.polygon(surface, color, self.points)
    def drawOutline(self, surface, color, width):
        pg.draw.lines(surface, color, False, self.points, width)
    def draw(self, surface):
        pg.draw.lines(surface, BLACK, True, self.points)
        if self.gameObject != None:
            self.gameObject.draw(surface)

#and my > (slope2 * mx) + b2 and my > (slope3 * mx) + b3 and my < (slope4 * mx) + b4 and my < (slope5 * mx) + b5 and my < (slope6 * mx) + b
