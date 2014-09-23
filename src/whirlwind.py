import technique
class Whirlwind(technique.Technique):
    def __init__(self):
        technique.Technique.__init__(self, "Whirlwind", None, 10, [])
        self.description = "The user spins their weapon around them, hurting all adjacent enemies."
        self.aoe = 2
        self.range = 1
        
        
