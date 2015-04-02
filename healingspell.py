import spell
class HealingSpell(spell.Spell):
    def __init__(self, name, target, effects = [], heal = 10):
        spell.Spell.__init__(self, name, target, effects)
        self.heal = heal
    def getHeal(self):
        return self.heal
