import party
class BattlePartyManager(party.Party):
    def __init__(self, party1, party2):
        self.party1 = party1
        self.party2 = party2
    def checkHero(self, hero):
        for x in self.party1.getHeroes():
            if x.getID() == hero.getID():
                return 1
        else:
            return 2
