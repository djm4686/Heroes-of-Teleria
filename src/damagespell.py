import spell
class DamageSpell(spell.Spell):
    def __init__(self, name, target, damage = 10, effects = []):
        spell.Spell.__init__(self, name, target, damage, effects)
