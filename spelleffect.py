__author__ = 'Admin'
class SpellEffect:

    def __init__(self, name, amt, duration = 1):
        self.name = name
        self.id = None
        self.duration = duration
        self.amt = amt
    def getAmt(self):
        return self.amt
    def applyToHero(self, h):
        for x in h.getSpellEffects():
            if x.id == self.id:
                return
        h.addSpellEffect(self)
    def removeFromHero(self, h):
        for x, y in zip(h.getSpellEffects(), range(len(h.getSpellEffects()))):
            if x.id == self.id:
                h.spellEffects.pop(y)
    def updateSpellEffect(self, hero):
        pass
    def isAttackMod(self):
        return False
    def isArmorMod(self):
        return False
    def isAttackMult(self):
        return False
    def isArmorMult(self):
        return False
    def isHitChanceMod(self):
        return False
    def isSlow(self):
        return False
    def isQuicken(self):
        return False
    def isDisable(self):
        return False
    def isRoundDuration(self):
        return False
    def isBurnDamage(self):
        return False
    def isSilence(self):
        return False
    def isCripple(self):
        return False
    def isMagicDamageMod(self):
        return False
    def isMagicResistMod(self):
        return False
    def statMod(self):
        return False