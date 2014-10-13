from isometrictile import *
class IsoBoard:
    def __init__(self, rows, cols, size = 50):
        self.tiles = []
        self.rows = rows
        self.cols = cols
        self.size = size
        self.generateBoard()
        self.setNeighbors()
    def getZone2(self):
        returns = []
        for x in self.tiles:
            for y in x:
                if y.getZone() == 2:
                    returns.append(y)
        return returns
    def getNeighborTiles(self, tile, r):
        if r == 1:
            return [tile]
        tiles = [tile]
        neighbors = tile.getNeighbors()
        for t in neighbors:
            if t != None:
                tiles += self.getNeighborTiles(t, r-1)
        tiles = list(set(tiles))
        return tiles
    def collidepoint(self, point):
        for row in self.tiles:
            for tile in row:
                if tile.collidepoint(point):
                    return tile
    def setNewCoords(self, coordDifference):
        for x in self.tiles:
            for y in x:
                y.x = y.x + coordDifference[0]
                y.y = y.y + coordDifference[1]
                y.reMakePoints()
    def setDirection(self, hero, point):
        tile = hero.getTile()
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
    def getZone1(self):
        returns = []
        for x in self.tiles:
            for y in x:
                if y.getZone() == 1:
                    returns.append(y)
        return returns
    def setNeighbors(self):
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[row])):
                if row != 0:
                    self.tiles[row][col].setN1(self.tiles[row - 1][col])
                if col != len(self.tiles[row])-1:
                    self.tiles[row][col].setN2(self.tiles[row][col + 1])
                if row != len(self.tiles) -1:
                    self.tiles[row][col].setN3(self.tiles[row+1][col])
                if col != 0:
                    self.tiles[row][col].setN4(self.tiles[row][col-1])
    def getTileIndeces(self, tile):
        for row in range(len(self.tiles)):
            for col in range(len(self.tiles[row])):
                if self.tiles[row][col].getID() == tile.getID():
                    return (col, row)
    def generateBoard(self):
        xcoord = 400
        ycoord = 100
        self.setStartCoords((xcoord, ycoord))
    def setStartCoords(self, coord):
        xcoord = coord[0]
        ycoord = coord[1]
        j = 0
        for row in range(self.rows):
            self.tiles.append([])
            for column in range(self.cols):
                if row > (self.rows-1) / 2:
                    self.tiles[row].append(IsometricTile(j, xcoord + (self.size * .5 * column) - (row * self.size * .5), ycoord + (row * self.size * .5 * .5) + (.5 * column * self.size * .5), size = self.size,  zone = 2))
                else:
                    self.tiles[row].append(IsometricTile(j, xcoord + (self.size * .5 * column) - (row * self.size * .5), ycoord + (row * self.size * .5 * .5) + (.5 * column * self.size * .5), size = self.size))
                j += 1
    def drawHeroes(self, surface):
        for row in self.tiles:
            for tile in row:
                tile.drawHero(surface)
    def drawTiles(self, surface):
        for row in self.tiles:
            for tile in row:
                tile.drawTile(surface)
        
