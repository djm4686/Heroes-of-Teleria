import ability
class Technique(ability.Ability):
    def __init__(self, name, target, damage, effects = []):
        ability.Ability.__init__(self, name, target, damage, target)
        self.type = "technique"
        self.effects = effects
    def getType(self):
        return self.type
    def getEffects(self):
        return self.effects
