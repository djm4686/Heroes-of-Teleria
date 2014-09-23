from shield import *
class Buckler(Shield):
    def __init__(self):
        Shield.__init__(self, "Buckler")
        self.ac = 5
    def getAC(self):
        return self.ac
