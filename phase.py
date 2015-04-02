class Phase:
    def __init__(self, name):
        self.name = name
        self.subphase = None
        self.parentPhase = None
    def getName(self):
        return self.name
    def addSubPhase(self, sub):
        sub.setParentPhase(self)
        self.subphase = sub
    def getSubPhase(self):
        return self.subphase
    def setParentPhase(self, p):
        self.parentPhase = p
    def getParentPhase(self):
        return self.parentPhase
