import party
class BattlePartyManager(party.Party):
    def __init__(self, party1, party2, playerID1 = 0, playerID2 = 0):
        self.party1 = party1
        self.party2 = party2
        self.playerID1 = playerID1
        self.playerID2 = playerID2
    def getHeroes(self):
        return self.party1 + self.party2
    def checkHero(self, hero):
        for x in self.party1.getHeroes():
            if x.getID() == hero.getID() and self.playerID1 == 0:
                return 1
            elif x.getID() == hero.getID() and self.playerID1 != 0:
                return self.playerID1
        else:
            if self.playerID2 == 0:
                return 2
            else:
                return self.playerID2