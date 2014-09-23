from meleeequipment import *
import firstaid
class Sword(MeleeWeapon):
    def __init__(self):
        MeleeWeapon.__init__(self, "Sword")
        self.power = 10
        self.ability = firstaid.FirstAid()
    def getPower(self):
        return self.power
