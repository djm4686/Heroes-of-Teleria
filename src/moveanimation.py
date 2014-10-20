import heroanimation, time, pygame, math
class Path:
    def __init__(self, startTile, startDirection):
        self.path = [startTile]
        self.directions = [startDirection]
        self.node = -1
    def addTile(self, tile, direction):
        self.path.append(tile)
        self.directions.append(direction)
    def getPath(self):
        return self.path
    def getDirections(self):
        return self.directions
    def getNextNode(self):
        self.node += 1
        if self.node < len(self.path):
            return self.path[self.node], self.directions[self.node]
        else:
            return None
        
class MoveAnimation(heroanimation.HeroAnimation):
    def __init__(self, startTile, endTile, hero):
        self.currentTile = startTile
        self.x, self.y = startTile.getCenter()
        self.startTile = startTile
        self.destTile = None
        self.hero = hero
        self.endTile = endTile
        self.lastTime = time.clock()
        self.curTime = time.clock()
        self.working = True
        self.node = None
        self.nextNode = None
        self.i = 0
        self.path = Path(startTile, self.hero.getDirection())
        self.createPath()
    def setDirection(self, tile, point, hero):
        x,y = point
        cx,cy = tile.getCenter()
        if x > cx and y < cy:
            hero.setDirection(1)
        if x < cx and y < cy:
            hero.setDirection(4)
        if x > cx and y > cy:
            hero.setDirection(2)
        if x < cx and y > cy:
            hero.setDirection(3)
    def createPath(self):
        currTile = self.hero.getTile()
        while (currTile.getID() != self.endTile.getID() and (currTile.getGameObject() != None and currTile.getGameObject().getID() == self.hero.getID())) or (currTile.getID() != self.endTile.getID() and currTile.getGameObject() == None) :
            self.setDirection(currTile, self.endTile.getCenter(), self.hero)
            currTile = self.hero.getTile().getNeighbors()[self.hero.getDirection()-1]
            self.hero.setTile(currTile)
            self.path.addTile(currTile, self.hero.getDirection())
        self.hero.setTile(self.startTile)
        self.hero.setDirection(self.path.getDirections()[1])
        print self.path.getDirections()
    def animate(self, surface):
        self.curTime = time.clock()
        if self.curTime - self.lastTime > .125 and self.working == True:
            if self.node != None:
                pass
            if self.hero.getTile() != None:
                if self.node == None:
                    self.node = self.path.getNextNode()
                    self.nextNode = self.path.getNextNode()
                    self.setDirection(self.node[0], self.nextNode[0].getCenter(), self.hero)
                    self.hero.setTile(None)
                elif self.nextNode != None:
                    self.node = self.nextNode
                    self.nextNode = self.path.getNextNode()
                    if self.nextNode != None:
                        self.setDirection(self.node[0], self.nextNode[0].getCenter(), self.hero)
                    self.hero.setTile(None)
                if self.nextNode == None:
                    self.working = False
                    self.hero.setTile(self.node[0])
                    return self.node
                self.lastTime = 0
            self.lastTime = self.curTime
            self.i += 1
            if self.i > 5:
                self.i = 0
        
        if self.nextNode != None and self.hero.getTile() == None:
            if self.x > self.nextNode[0].getCenter()[0] and self.y > self.nextNode[0].getCenter()[1]:
                self.x -= 1
                self.y = (.5 * self.x) + (self.nextNode[0].getCenter()[1] - (.5 * self.nextNode[0].getCenter()[0]))
            elif self.x < self.nextNode[0].getCenter()[0] and self.y > self.nextNode[0].getCenter()[1]:
                self.x += 1
                self.y = (-.5 * self.x) + (self.nextNode[0].getCenter()[1] - (-.5 * self.nextNode[0].getCenter()[0]))
            elif self.x < self.nextNode[0].getCenter()[0] and self.y < self.nextNode[0].getCenter()[1]:
                self.x += 1
                self.y = (.5 * self.x) + (self.nextNode[0].getCenter()[1] - (.5 * self.nextNode[0].getCenter()[0]))
            elif self.x > self.nextNode[0].getCenter()[0] and self.y < self.nextNode[0].getCenter()[1]:
                self.x -= 1
                self.y = (-.5 * self.x) + (self.nextNode[0].getCenter()[1] - (-.5 * self.nextNode[0].getCenter()[0]))
            if self.nextNode != None and math.fabs(self.x - self.nextNode[0].getCenter()[0]) < 1 and math.fabs(self.y - self.nextNode[0].getCenter()[1]) < 1:
                self.hero.setTile(self.nextNode[0])
            if self.nextNode == None:
                self.hero.setTile(self.node[0])
            if self.hero.getTile != None:
                sprites = self.hero.getWalkingSprites()
                p = pygame.Rect(self.x, self.y, 60, 60)
                p.center = (self.x, self.y - 20)
                surface.blit(sprites[self.i],p)





            
