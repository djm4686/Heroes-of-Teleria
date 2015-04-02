import hextile
class GameTile(hextile.HexTile):
    def __init__(self, ide, x = 0, y = 0, size = 50, zone = 1):
        hextile.HexTile.__init__(self, ide, x, y, size, zone)
        self.entity = None
        self.terrain = None
    def setEntity(self, entity):
        self.entity = entity
    def setTerrain(self, terrain):
        self.terrain = terrain
    def getEntity(self):
        return self.entity
    def getTerrain(self):
        return self.terrain
	def draw(self, surface):
		pg.draw.lines(surface, BLACK, False, self.points)
		if self.terrain != None:
			self.terrain.draw(surface)
		if self.entity != None:
			self.entity.draw(surface)
