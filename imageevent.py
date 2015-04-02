import battlevent
class ImageEvent(battlevent.BattleEvent):
    def __init__(self, ide, image, tile):
        battlevent.BattleEvent.__init__(self, ide, tile, (0,0,0))
        self.image = image
        self.tile = tile
    def draw(self, surface):
        r = self.image.get_rect()
        r.center = self.tile.getCenter()
        r.y = r.y - 20
        surface.blit(self.image, r)
