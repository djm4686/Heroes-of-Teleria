from shield import *
class HeavyShield(Shield):
    def __init__(self):
        Shield.__init__(self, "HeavyShield")
        self.ac = 9
    def getAC(self):
        return self.ac
