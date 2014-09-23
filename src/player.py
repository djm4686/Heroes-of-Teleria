import party
class Player:
    def __init__(self, ide, name, party = party.AI):
        self.name = name
        self.id = ide
        self.party = party
    def getID(self):
        return self.id
    def getName(self):
        return self.name
    def getParty(self):
        return self.party
