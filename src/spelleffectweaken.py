__author__ = 'Admin'
import spelleffect

class EffectWeaken(spelleffect.SpellEffect):

    def __init__(self, amt):
        spelleffect.SpellEffect.__init__(self, "Weaken", amt, 2)
        self.id = 1

    def updateSpellEffect(self, hero):
        self.duration -= 1
        if self.duration < 0:
            return False
        return True

    def isRoundDuration(self):
        return True

    def isAttackMod(self):
        return True

