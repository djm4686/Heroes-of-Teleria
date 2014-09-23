import technique
class FirstAid(technique.Technique):
    def __init__(self):
        technique.Technique.__init__(self, "First Aid", None,10, [])
        self.aoe = 1
        self.description = "The user practices first aid on himself, healing wounds slightly."
