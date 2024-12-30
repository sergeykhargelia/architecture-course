import random
from imob_strategy import IMobStrategy

# Make random moves
class RandomMobStrategy(IMobStrategy):
    def make_move(self, map_state, mob_position, character_position):
        return random.choice(map_state.get_allowed_neighbours(mob_position))

# Just stay in the same place
class PassiveMobStrategy(IMobStrategy):
    def make_move(self, map_state, mob_position, character_position):
        return mob_position

# Make a move that bring mob closer to the character (in terms of Manhattan distance)
class AggressiveMobStrategy(IMobStrategy):
    def make_move(self, map_state, mob_position, character_position):
        positions = map_state.get_allowed_neighbours(mob_position)
        return min(positions, key=lambda pos: \
                   abs(pos[0] - character_position[0]) + abs(pos[1] - character_position[1]))

class IMobStrategyGenerator:
    def generate_strategy_by_id(id):
        pass

class MobStrategyGenerator(IMobStrategyGenerator):
    def generate_strategy_by_id(self, id):
        if id == 0:
            return PassiveMobStrategy()
        elif id < 3:
            return RandomMobStrategy()
        else:
            return AggressiveMobStrategy()