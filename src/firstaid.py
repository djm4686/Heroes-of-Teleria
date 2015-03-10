import spell

class FirstAid(spell.Spell):

    def __init__(self):
        spell.Spell.__init__(self, "First Aid", 10)
        self.range = 1
        self.description = "This hero uses his First Aid skills to heal himself in battle."
    def target(self, t):
        t.heal(self.damage)
