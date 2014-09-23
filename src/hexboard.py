import gametile, line

class HexBoard:
    def __init__(self, rows, cols, size = 50):
        self.tiles = []
        self.rows = rows
        self.cols = cols
        self.size = size
        self.generateBoard()
        self.setNeighbors()
    def getTileIndeces(self, tile):
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[row])):
                if self.tiles[row][col].getID() == tile.getID():
                    return (col, row)
    def generateBoard(self):
        xcoord = 100
        ycoord = 100
        self.setStartCoords((xcoord, ycoord))
    def getZone1(self):
        returns = []
        for x in self.tiles:
            for y in x:
                if y.getZone() == 1:
                    returns.append(y)
        return returns
    def getZone2(self):
        returns = []
        for x in self.tiles:
            for y in x:
                if y.getZone() == 2:
                    returns.append(y)
        return returns
    def addTile(self, tile):
        self.tiles.append(tile)
    def collidepoint(self, point):
        for row in self.tiles:
            for tile in row:
                if tile.collidepoint(point):
                    return tile
        return None
    def setNeighbors(self):
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                try:
                    if y != 0:
                        if y % 2 == 0  and x != 0:
                            self.tiles[y][x].setN1(self.tiles[y-1][x-1])
                        if y % 2 == 1:
                            self.tiles[y][x].setN1(self.tiles[y-1][x])
                except IndexError:
                    self.tiles[y][x].setN1(None)
                try:
                    if y != 0:
                        if y % 2 == 0:
                            self.tiles[y][x].setN2(self.tiles[y-2][x])
                        if y % 2 == 1 and y != 1:
                            self.tiles[y][x].setN2(self.tiles[y-2][x])
                except IndexError:
                    self.tiles[y][x].setN2(None)
                try:
                    if y != 0:
                        if y % 2 == 0:
                            self.tiles[y][x].setN3(self.tiles[y-1][x])
                        if y % 2 == 1:
                            self.tiles[y][x].setN3(self.tiles[y-1][x+1])
                except IndexError:
                    self.tiles[y][x].setN3(None)
                try:
                    if y % 2 == 0:
                        self.tiles[y][x].setN4(self.tiles[y+1][x])
                    if y % 2 == 1:
                        self.tiles[y][x].setN4(self.tiles[y+1][x+1])
                except IndexError:
                    self.tiles[y][x].setN4(None)
                try:
                    if y % 2 == 0:
                        self.tiles[y][x].setN5(self.tiles[y+2][x])
                    if y % 2 == 1:
                        self.tiles[y][x].setN5(self.tiles[y+2][x])
                except IndexError:
                    self.tiles[y][x].setN5(None)
                try:
                    if y % 2 == 0 and x != 0:
                        self.tiles[y][x].setN6(self.tiles[y+1][x-1])
                    if y % 2 == 1:
                        self.tiles[y][x].setN6(self.tiles[y+1][x])
                except IndexError:
                    self.tiles[y][x].setN6(None)
    def setDirection(self, hero, point):
        tile = hero.getTile()
        cones = []
        for x in range(len(tile.points)):
            if x == 6:
                break
            else:
                cones.append((line.Line(tile.points[x], tile.getCenter()), line.Line(tile.points[x+1], tile.getCenter())))
        for cone in range(len(cones)):
            if cone == 0:
                if cones[cone][0].isPointGreaterThan(point) and cones[cone][1].isPointLessThan(point):
                    hero.setDirection(1)
            if cone == 1:
                if cones[cone][0].isPointGreaterThan(point) and cones[cone][1].isPointGreaterThan(point):
                    hero.setDirection(2)
            if cone == 2:
                if cones[cone][0].isPointLessThan(point) and cones[cone][1].isPointGreaterThan(point):
                    hero.setDirection(3)
            if cone == 3:
                if cones[cone][0].isPointLessThan(point) and cones[cone][1].isPointGreaterThan(point):
                    hero.setDirection(4)
            if cone == 4:
                if cones[cone][0].isPointLessThan(point) and cones[cone][1].isPointLessThan(point):
                    hero.setDirection(5)
            if cone == 5:
                if cones[cone][0].isPointGreaterThan(point) and cones[cone][1].isPointLessThan(point):
                    hero.setDirection(6)
    def drawTiles(self, surface):
        for row in self.tiles:
            for tile in row:
                tile.draw(surface)
    def setNewCoords(self, coordDifference):
        for x in self.tiles:
            for y in x:
                y.x = y.x + coordDifference[0]
                y.y = y.y + coordDifference[1]
                y.reMakePoints()
    def setStartCoords(self, coord):
        xcoord = coord[0]
        ycoord = coord[1]
        j = 0
        for i in range(self.rows):
            self.tiles.append([])
            for x in range(self.cols):
                if i % 2 == 0:
                    if i > self.rows/2:
                        self.tiles[i].append(gametile.GameTile(ide = j, x = xcoord + (x * 1.5 * self.size), y = ycoord + (i/2 * self.size), size = self.size, zone = 2))
                    else:
                        self.tiles[i].append(gametile.GameTile(ide = j, x = xcoord + (x * 1.5 * self.size), y = ycoord + (i/2 * self.size), size = self.size))
                else:
                    if i > self.rows/2:
                        self.tiles[i].append(gametile.GameTile(ide = j, x = xcoord + (x * 1.5 * self.size) + (self.size * .75), y = ycoord + (i * self.size * .5), size = self.size, zone = 2))
                    else:
                        self.tiles[i].append(gametile.GameTile(ide = j, x = xcoord + (x * 1.5 * self.size) + (self.size * .75), y = ycoord + (i * self.size * .5), size = self.size))
                j = j + 1
    def draw(self, surface):
        for row in self.tiles:
            for tile in row:
                tile.draw(surface)
        