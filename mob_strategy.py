import random
from imob_strategy import IMobStrategy

# Make random moves
class RandomMobStrategy(IMobStrategy):
    def __init__(self, map_state):
        super().__init__(map_state)

    def make_move(self, mob_position, character_position):
        return random.choice(super()._get_allowed_neighbours(mob_position))

# Just stay in the same place
class PassiveMobStrategy(IMobStrategy):
    def __init__(self, map_state):
        super().__init__(map_state)

    def make_move(self, mob_position, character_position):
        return mob_position

# Make a move that bring mob closer to the character (in terms of Manhattan distance)
class AggressiveMobStrategy(IMobStrategy):
    def __init__(self, map_state):
        super().__init__(map_state)
    
    def make_move(self, mob_position, character_position):
        positions = super()._get_allowed_neighbours(mob_position)
        return min(positions, key=lambda pos: \
                   abs(pos[0] - character_position[0]) + abs(pos[1] - character_position[1]))

# Get a strategy for i-th mob on the map
def get_strategy_by_id(id):
    if id == 0:
        return PassiveMobStrategy
    elif id < 3:
        return RandomMobStrategy
    else:
        return AggressiveMobStrategy