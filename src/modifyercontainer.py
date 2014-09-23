class ModifyerContainer:
    def __init__(self, strength, agi, con, intell, wis):
        self.str = strength
        self.agi = agi
        self.con = con
        self.inte = intell
        self.wis = wis
    def getWisdomModifyer(self):
        return self.wis
    def getStrengthModifyer(self):
        return self.str
    def getAgilityModifyer(self):
        return self.agi
    def getConstitutionModifyer(self):
        return self.con
    def getIntelligenceModifyer(self):
        return self.inte
