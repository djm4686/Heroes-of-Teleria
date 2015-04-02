from meleeequipment import *
import firstaid
import spellweaken
class BroadSword(MeleeWeapon):
    def __init__(self):
        MeleeWeapon.__init__(self, "Broadsword")
        self.power = 12
        self.spell = spellweaken.Weaken()
    def getPower(self):
        return self.power
