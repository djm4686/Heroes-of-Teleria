from shield import *
class RoundShield(Shield):
    def __init__(self):
        Shield.__init__(self, "Round Shield")
        self.ac = 7
    def getAC(self):
        return self.ac
