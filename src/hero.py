import random, math, sword, shortbow, buckler, chainmail, heroconfigscreen, pygame, time
from globalvars import *
class Hero:
    def __init__(self, ID, name, heroclass, race, playerID = 0):
        pygame.init()
        self.ID = ID
        self.name = name
        self.activeHeroClass = heroclass
        self.secondaryClasses = []
        self.race = race
        self.playerID = playerID
        self.level = 1
        self.exp = 0
        self.expForNextLevel = 100
        self.strength = 10
        self.direction = 5
        self.agility = 10
        self.font = pygame.font.Font(pygame.font.get_default_font(), 10)
        self.nameLabel = self.font.render(self.name, True, (255,255,255),(0,0,0))
        self.constitution = 5
        self.intelligence = 10
        self.wisdom = 10
        self.maxhp = 20 + random.randrange(1, self.activeHeroClass.getHpMod())
        self.maxMana = 20 + random.randrange(1, self.activeHeroClass.getManaMod())
        self.currentHp = self.maxhp
        self.currentMana = self.maxMana
        self.armor = None
        self.tile = None
        self.range = 2
        self.meleeWeapon = sword.Sword()
        self.rangedWeapon = shortbow.ShortBow()
        self.shield = buckler.Buckler()
        self.armor = chainmail.ChainMail()
        self.lastTime = time.clock()
        self.i = 0
    def getPlayerID(self):
        return self.playerID
    def getExp(self):
        return self.exp
    def addExp(self, exp):
        self.exp += exp
        if self.exp > self.expForNextLevel:
            self.exp -= self.expForNextLevel
            self.levelUp()
        self.expForNextLevel += int(self.expForNextLevel * .5)
    def getJSON(self):
        return  ("{" +
                 " \"heroID\" : \"" + str(self.ID) + "\"," +
                 " \"name\" : \"" + self.name + "\"," +
                 " \"level\" : \"" + str(self.level) + "\"," +
                 " \"exp\" : \"" + str(self.exp) + "\"," +
                 " \"str\" : \"" + str(self.strength) + "\"," +
                 " \"agi\" : \"" + str(self.agility) + "\"," +
                 " \"con\" : \"" + str(self.constitution) + "\"," +
                 " \"inte\" : \"" + str(self.intelligence) + "\"," +
                 " \"wis\" : \"" + str(self.wisdom) + "\"," +
                 " \"hp\" : \"" + str(self.maxhp) + "\"," +
                 " \"activeClass\" : \"" + str(getClassesIndex(self.activeHeroClass)) + "\","
                 " \"race\" : \"" + str(getRacesIndex(self.race)) + "\","
                 " \"meleeEquipment\" : \"" + str(getMeleeWeaponIndex(self.meleeWeapon)) + "\","
                 " \"rangedEquipment\" : \"" + str(getRangedWeaponIndex(self.rangedWeapon)) + "\","
                 " \"armorEquipment\" : \"" + str(getArmorIndex(self.armor)) + "\","
                 " \"shieldEquipment\" : \"" + str(getShieldIndex(self.shield)) + "\","
                 " \"currenthp\" : \"" + str(self.currentHp) + "\"," +
                 " \"playerID\" : \"" + str(self.playerID) + "\"," +
                 " \"mana\" : \"" + str(self.maxMana) + "\"," +
                 " \"currentmana\" : \"" + str(self.currentMana) + "\"}").encode("ascii", "ignore")
    
    def setID(self, ID):
        self.ID = ID
    def isDead(self):
        return (self.currentHp <= 0)
    def setTile(self, tile):
        self.tile = tile
    def getTile(self):
        return self.tile
    def getInitiative(self):
        return self.agility/self.level
    def damageSelf(self, damage):
        self.currentHp = self.currentHp - damage
        if self.currentHp < 0:
            self.currentHp = 0
        return damage
    def useMana(self, mana):
        self.currentMana = self.currentMana - mana
        if self.currentMana < 0:
            self.currentMana = 0
    def levelUp(self):
        self.level = self.level + 1
        if self.race.getName() == "Human":
            self.strength = int(self.strength + math.ceil(random.randrange(1,4) * self.activeHeroClass.getModifyers().getStrengthModifyer()))
            self.agility = int(self.agility + math.ceil(random.randrange(1,4) * self.activeHeroClass.getModifyers().getAgilityModifyer()))
            self.constitution = int(self.constitution + math.ceil(random.randrange(1,4) * self.activeHeroClass.getModifyers().getConstitutionModifyer()))
            self.wisdom = int(self.wisdom + math.ceil(random.randrange(1,4) * self.activeHeroClass.getModifyers().getWisdomModifyer()))
            self.intelligence = int(self.intelligence + math.ceil(random.randrange(1,4) * self.activeHeroClass.getModifyers().getIntelligenceModifyer()))
        else:
            self.strength = int(self.strength + math.ceil(random.randrange(1,self.race.getModifyers().getStrengthModifyer()) * self.activeHeroClass.getModifyers().getStrengthModifyer()))
            self.agility = int(self.agility + math.ceil(random.randrange(1,self.race.getModifyers().getAgilityModifyer()) * self.activeHeroClass.getModifyers().getAgilityModifyer()))
            self.constitution = int(self.constitution + math.ceil(random.randrange(1,self.race.getModifyers().getConstitutionModifyer()) * self.activeHeroClass.getModifyers().getConstitutionModifyer()))
            self.wisdom = int(self.wisdom + math.ceil(random.randrange(1,self.race.getModifyers().getWisdomModifyer()) * self.activeHeroClass.getModifyers().getWisdomModifyer()))
            self.intelligence = int(self.intelligence + math.ceil(random.randrange(1,self.race.getModifyers().getIntelligenceModifyer()) * self.activeHeroClass.getModifyers().getIntelligenceModifyer()))
        self.levelHP()
        self.levelMana
    def setDirection(self, d):
        self.direction = d
    def rotateImage(self, image):
        if self.direction == 1:
            return pygame.transform.rotate(image, -120)
        elif self.direction == 2:
            return pygame.transform.rotate(image, 180)
        elif self.direction == 3:
            return pygame.transform.rotate(image, 120)
        elif self.direction == 4:
            return pygame.transform.rotate(image, 60)
        elif self.direction == 5:
            return image
        elif self.direction == 6:
            return pygame.transform.rotate(image, -60)
    def getRangedRange(self):
        return self.rangedWeapon.getRange()
    def getDirection(self):
        return self.direction
    def getID(self):
        return self.ID
    def getMovementRange(self):
        return self.range + 1
    def meleeAttack(self, hero):
        return hero.damageSelf(int(math.ceil((self.strength +self.getMeleeWeapon().getPower())* hero.calculateAC())))
    def rangedAttack(self, hero):
        return hero.damageSelf(int(math.ceil((self.agility + self.getRangedWeapon().getPower())*hero.calculateAC())))
    def getMaxMana(self):
        return self.maxMana
    def makeConfigScreen(self, params):
        return heroconfigscreen.HeroConfigScreen(self, params[0])
    def calculateMeleeDamage(self):
        return (self.strength + self.meleeWeapon.getDamage())/self.level
    def calculateRangedDamage(self):
        return (self.agility + self.rangedWeapon.getDamage())/self.level
    def calculateAC(self):
        return (.06 * self.getArmor().getAC())/(1+(.06 * self.getArmor().getAC()))
    def getAC(self):
        return self.armor
    def calculateMissChance(self, mod):
        pass
    def networkedLevelup(self):
        pass
    def getCurrentHP(self):
        return self.currentHp
    def levelMana(self):
        self.maxMana = int(self.mana + math.ceil(self.intelligence+self.wisdom/2/self.level + random.randrange(1, self.activeHeroClass.getManaMod())))                           
    def levelHP(self):
        self.maxhp = int(self.maxhp + math.ceil(self.constitution/self.level + random.randrange(1,self.activeHeroClass.getHpMod())))
    def getName(self):
        return self.name
    def getRace(self):
        return self.race
    def getSecondaryClasses(self):
        return self.secondaryClasses
    def getActiveHeroClass(self):
        return self.activeHeroClass
    def getLevel(self):
        return self.level
    def getMaxHp(self):
        return self.maxhp
    def getStr(self):
        return self.strength
    def getAgi(self):
        return self.agility
    def getCon(self):
        return self.constitution
    def getInt(self):
        return self.intelligence
    def getWis(self):
        return self.wisdom
    def getArmor(self):
        return self.armor
    def getMeleeWeapon(self):
        return self.meleeWeapon
    def getRangedWeapon(self):
        return self.rangedWeapon
    def getShield(self):
        return self.shield
    def getCurrentHp(self):
        return self.currentHp
    def getCurrentMana(self):
        return self.currentMana
    def draw(self, surface):
        if not self.isDead():
            currtime = time.clock()
            if self.direction == 1:
                sprites = self.activeHeroClass.getD1Sprites()
            elif self.direction == 2:
                sprites = self.activeHeroClass.getD2Sprites()
            elif self.direction == 3:
                sprites = self.activeHeroClass.getD3Sprites()
            elif self.direction == 4:
                sprites = self.activeHeroClass.getD4Sprites()
            elif self.direction == 5:
                sprites = self.activeHeroClass.getD5Sprites()
            elif self.direction == 6:
                sprites = self.activeHeroClass.getD6Sprites()
            
            r = pygame.Rect(self.tile.getCenter(), (sprites[0+self.i].get_rect().width, sprites[0+self.i].get_rect().height))
            r.center = self.tile.getCenter()
            surface.blit(sprites[0+self.i], r)
            if currtime - self.lastTime > .5:
                self.i += 1
                self.lastTime = currtime
                if self.i > 2:
                    self.i = 0
            r = pygame.Rect(self.tile.getCenter(), (self.nameLabel.get_rect().width, self.nameLabel.get_rect().height))
            r.center = self.tile.getCenter()
            r.y = r.y - 30
            surface.blit(self.nameLabel, r)
            hpLabel = self.font.render("HP: " + str(self.getCurrentHP()), True, (0,0,0), (255,0,0))
            r = pygame.Rect(self.tile.getCenter(), (hpLabel.get_rect().width, hpLabel.get_rect().height))
            r.center = self.tile.getCenter()
            r.y = r.y - 20
            surface.blit(hpLabel, r)
        else:
            i = pygame.image.load("images/tombstone.png")
            r = pygame.Rect(self.tile.getCenter(), (i.get_rect().width, i.get_rect().height))
            r.center = self.tile.getCenter()
            surface.blit(i, r)
def createFromJSON(data):
        h = Hero(int(data["heroID"]), data["name"], CLASSES[int(data["activeClass"])], RACES[int(data["race"])])
        h.level = int(data["level"])
        h.exp = int(data["exp"])
        h.strength = int(data["str"])
        h.agility = int(data["agi"])
        h.constitution = int(data["con"])
        h.intelligence = int(data["inte"])
        h.wisdom = int(data["wis"])
        h.maxhp = int(data["hp"])
        h.playerID = int(data["playerID"])
        h.meleeWeapon = MELEE_WEAPONS[int(data["meleeEquipment"])]
        h.rangedWeapon = RANGED_WEAPONS[int(data["rangedEquipment"])]
        h.armor = ARMOR[int(data["armorEquipment"])]
        h.shield = SHIELDS[int(data["shieldEquipment"])]
        h.maxMana = int(data["mana"])
        h.currentHp = int(data["currenthp"])
        h.currentMana = int(data["currentmana"])
        return h
