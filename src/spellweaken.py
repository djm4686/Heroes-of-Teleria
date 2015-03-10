__author__ = 'Admin'
import spell
import spelleffectweaken
class Weaken(spell.Spell):
    def __init__(self):
        spell.Spell.__init__(self, "Weaken", 0, [spelleffectweaken.EffectWeaken(-10)])
        self.description = "Weakens an enemy Hero within 1 tile. Causes the target to do reduced damage on attacks."
    def target(self, t):
        t.addSpellEffect(self.effects[0])

