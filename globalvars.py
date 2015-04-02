import classhealer, classfighter, classmage, classarcher
import sword, broadsword, pike, greatsword
import human, elf, dwarf, halfling
import shortbow, longbow, throwingknife
import chainmail, platemail, scalemail
import roundshield, buckler, heavyshield


CLASSES = [ classfighter.ClassFighter(),
            classmage.ClassMage(),
            classarcher.ClassArcher()]
RACES = [ human.Human(),
          dwarf.Dwarf(),
          halfling.Halfling(),
          elf.Elf()]
NAMES = open("fantasy_names.txt", "r").readlines()
for x in range(len(NAMES)):
    NAMES[x] = "".join(NAMES[x].split("\n"))

MELEE_WEAPONS = [sword.Sword(),
                 broadsword.BroadSword(),
#                 pike.Pike(),
                 greatsword.GreatSword()]
RANGED_WEAPONS = [shortbow.ShortBow(),
                  longbow.LongBow(),
                  throwingknife.ThrowingKnife()]
ARMOR = [chainmail.ChainMail(),
         platemail.PlateMail(),
         scalemail.ScaleMail()]
SHIELDS = [roundshield.RoundShield(),
           buckler.Buckler(),
           heavyshield.HeavyShield()]
def getRacesIndex(w):
    for x in range(len(RACES)):
        if w.name == RACES[x].name:
            return x
def getClassesIndex(w):
    for x in range(len(CLASSES)):
        if w.name == CLASSES[x].name:
            return x
def getMeleeWeaponIndex(w):
    for x in range(len(MELEE_WEAPONS)):
        if w.name == MELEE_WEAPONS[x].name:
            return x
def getRangedWeaponIndex(w):
    for x in range(len(RANGED_WEAPONS)):
        if w.name == RANGED_WEAPONS[x].name:
            return x
def getArmorIndex(w):
    for x in range(len(ARMOR)):
        if w.name == ARMOR[x].name:
            return x
def getShieldIndex(w):
    for x in range(len(SHIELDS)):
        if w.name == SHIELDS[x].name:
            return x
