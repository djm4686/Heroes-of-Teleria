from meleeequipment import *
import spellweaken
class Staff(MeleeWeapon):
    def __init__(self):
        MeleeWeapon.__init__(self, "Staff")
        self.power = 6
        self.spell = spellweaken.Weaken()
    def getPower(self):
        return self.power
