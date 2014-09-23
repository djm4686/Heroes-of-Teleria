import ability
class Spell(ability.Ability):
    def __init__(self, name, target, effects = []):
        ability.Ability.__init__(self, name, target, effects)
        self.type = "spell"
    def getType(self):
        return self.type
