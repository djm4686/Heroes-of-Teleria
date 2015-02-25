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
            return self.path[self.node]
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
        start = self.startTile
        start.gscore = 0
        start.last = None
        dest = self.endTile
        closedSet = []
        openSet = [start]
        self.heuristic = lambda current: math.sqrt(abs(current.getCenter()[1] - dest.getCenter()[1])**2 + abs(current.getCenter()[0] - dest.getCenter()[0])**2)/60
        while len(openSet) > 0:
            current = sorted(openSet, key=lambda x: self.heuristic(x))[0]
            if dest.getID() == current.getID() or current.getID() == dest.getID():
                self.path.path = self.reconstructPath(current)
            closedSet.append(openSet.pop(0))
            for neighbor in current.getNeighbors():
                if neighbor == None or self.checkTileID(closedSet, neighbor.getID()) or neighbor.getGameObject() != None:
                    continue
                tentgscore = current.gscore + 1
                if not self.checkTileID(openSet, neighbor.getID()):
                    neighbor.gscore = tentgscore
                    neighbor.last = current
                    neighbor.fscore = neighbor.gscore + self.heuristic(neighbor)
                    if not self.checkTileID(closedSet, neighbor.getID()):
                        openSet.append(neighbor)
        return False
    def checkTileID(self, tiles, id):
        for x in tiles:
            if x and x.getID() == id:
                return True
        else:
            return False
    def reconstructPath(self, current):
        total_path = [current]
        while current.last:
            total_path.append(current.last)
            current = current.last
        return total_path[::-1]

    def animate(self, surface):
        self.curTime = time.clock()
        if self.curTime - self.lastTime > .125 and self.working == True:
            if self.node != None:
                pass
            if self.hero.getTile() != None:
                if self.node == None:
                    self.node = self.path.getNextNode()
                    self.nextNode = self.path.getNextNode()
                    self.setDirection(self.node, self.nextNode.getCenter(), self.hero)
                    self.hero.setTile(None)
                elif self.nextNode != None:
                    self.node = self.nextNode
                    self.nextNode = self.path.getNextNode()
                    if self.nextNode != None:
                        self.setDirection(self.node, self.nextNode.getCenter(), self.hero)
                    self.hero.setTile(None)
                if self.nextNode == None:
                    self.working = False
                    self.hero.setTile(self.node)
                    print "Returning node!"
                    return self.node
                self.lastTime = 0
            self.lastTime = self.curTime
            self.i += 1
            if self.i > 5:
                self.i = 0
        
        if self.nextNode != None and self.hero.getTile() == None:
            if self.x > self.nextNode.getCenter()[0] and self.y > self.nextNode.getCenter()[1]:
                self.x -= 2
                self.y = (.5 * self.x) + (self.nextNode.getCenter()[1] - (.5 * self.nextNode.getCenter()[0]))
            elif self.x < self.nextNode.getCenter()[0] and self.y > self.nextNode.getCenter()[1]:
                self.x += 2
                self.y = (-.5 * self.x) + (self.nextNode.getCenter()[1] - (-.5 * self.nextNode.getCenter()[0]))
            elif self.x < self.nextNode.getCenter()[0] and self.y < self.nextNode.getCenter()[1]:
                self.x += 2
                self.y = (.5 * self.x) + (self.nextNode.getCenter()[1] - (.5 * self.nextNode.getCenter()[0]))
            elif self.x > self.nextNode.getCenter()[0] and self.y < self.nextNode.getCenter()[1]:
                self.x -= 2
                self.y = (-.5 * self.x) + (self.nextNode.getCenter()[1] - (-.5 * self.nextNode.getCenter()[0]))
            if self.nextNode != None and math.fabs(self.x - self.nextNode.getCenter()[0]) < 1 and math.fabs(self.y - self.nextNode.getCenter()[1]) < 1:
                self.hero.setTile(self.nextNode)
            if self.nextNode == None:
                self.hero.setTile(self.node)
            if self.hero.getTile != None:
                sprites = self.hero.getWalkingSprites()
                p = pygame.Rect(self.x, self.y, 60, 60)
                p.center = (self.x, self.y - 20)
                surface.blit(sprites[self.i],p)





            
