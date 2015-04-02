__author__ = 'Admin'
import spell


class Fireball(spell.Spell):

    def __init__(self):
        spell.Spell.__init__(self, "Fireball", 12, rang=4, aoe=2)
        self.description = "The Hero creates fire from nothing and hurls it, hitting friend and foe alike."

    def target(self, t):
        n = t.getTile().getNeighbors()
        for tile in n:
            if tile != None and tile.getGameObject() != None:
                tile.getGameObject().damageSelf(self.damage)
        t.damageSelf(self.damage)

    def targetsGround(self):
        return True