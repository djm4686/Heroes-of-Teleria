from meleeequipment import *
import spellfireball

class GreatSword(MeleeWeapon):
    def __init__(self):
        MeleeWeapon.__init__(self, "Greatsword")
        self.power = 14
        self.spell = spellfireball.Fireball()
    def getPower(self):
        return self.power
