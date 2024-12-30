from character import Character
from inventory import Inventory
from mob import Mob

class ICharacterGenerator:
    def generate_character(self, position):
        pass

class IMobGenerator:
    def generate_mob(self, position, id):
        pass
    
class SimpleCharacterGenerator(ICharacterGenerator):
    def __init__(self, previous_character=None):
        self._previous_character = previous_character

    def generate_character(self, position):
        if self._previous_character:
            character = self._previous_character.clone()
            character.change_position(position)
        else:
            character = Character(
                'C',
                Inventory(),
                position
            )

        return character

class SimpleMobGenerator(IMobGenerator):
    def __init__(self, mob_strategy_generator):
        self._mob_strategy_generator = mob_strategy_generator
    
    def generate_mob(self, position, id):
        name = f'mob{id + 1}'
        strategy = self._mob_strategy_generator.generate_strategy_by_id(id)
        return Mob(name, strategy, position)