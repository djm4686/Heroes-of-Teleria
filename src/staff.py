from meleeequipment import *
import fireball
class Staff(MeleeWeapon):
    def __init__(self):
        MeleeWeapon.__init__(self, "Broadsword")
        self.power = 6
        self.ability = fireball.Fireball()
    def getPower(self):
        return self.power
