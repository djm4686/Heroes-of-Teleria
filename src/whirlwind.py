import spell
class Whirlwind(spell.Spell):
    def __init__(self):
        apell.Spell.__init__(self, "Whirlwind", 10, [])
        self.description = "The user spins their weapon around them, hurting all adjacent enemies."
        self.aoe = 2
        self.range = 1
        
        
