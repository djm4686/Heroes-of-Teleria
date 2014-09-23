import damagespell
class Fireball(damagespell.DamageSpell):
    def __init__(self):
        damagespell.DamageSpell.__init__(self, "Fireball", None, 10, [])
        self.description = "The user creates a ball of fire that explodes at target location"
        self.aoe = 2
        self.range = 4
        self.friendlyFire = True
