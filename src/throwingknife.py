from rangedequipment import *
class ThrowingKnife(RangedWeapon):
    def __init__(self):
        RangedWeapon.__init__(self, "Throwing Knife")
        self.power = 10
    def getPower(self):
        return self.power
