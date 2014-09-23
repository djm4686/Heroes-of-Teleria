from meleeequipment import *
import firstaid
class BroadSword(MeleeWeapon):
    def __init__(self):
        MeleeWeapon.__init__(self, "Broadsword")
        self.power = 12
        self.ability = firstaid.FirstAid()
    def getPower(self):
        return self.power
