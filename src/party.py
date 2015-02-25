import random, hero
from globalvars import *
class Party:
    def __init__(self, player):
        self.name = ""
        self.player = player
        self.heroes = []
    def getPlayer(self):
        return self.player
    def addHero(self, hero):
        self.heroes.append(hero)
    def getHeroes(self):
        return self.heroes
    def getHeroByName(self, name):
        for x in self.heroes:
            if x.getName() == name:
                return x
def makeHero(ide):
        return hero.Hero(ide, random.choice(NAMES), heroclass = random.choice(CLASSES), race = random.choice(RACES))
AI = Party(0)
AI2 = Party(0)
for x in range(1):
    AI.addHero(makeHero(x + 10))
    AI2.addHero(makeHero(x+15))
def getAi():
    AI = Party(0)
    for x in range(1):
        AI.addHero(makeHero(x+10))
    return AI

