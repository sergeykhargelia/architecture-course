import unittest

from game_state.game_state import GameState
from util.direction import Direction

def _get_map(game_state):
    return game_state.get_view()['map']['grid']

def _find_character_position(game_state):
    map_view = _get_map(game_state)
    for i in range(len(map_view[0])):
        for j in range(len(map_view[1])):
            if map_view[i][j] == 'C':
                return (i, j)

def _find_valid_direction(game_state, pos):
    map_view = _get_map(game_state)
    for delta, dir in [
        ((0, 1), Direction.RIGHT), 
        ((0, -1), Direction.LEFT), 
        ((1, 0), Direction.DOWN), 
        ((-1, 0), Direction.UP)
    ]:
        new_pos = (pos[0] + delta[0], pos[1] + delta[1])
        if new_pos[0] >= 0 and new_pos[1] >= 0 and \
            new_pos[0] < len(map_view) and new_pos[1] < len(map_view[0]) and \
            map_view[new_pos[0]][new_pos[1]] == '':
                return new_pos, dir
        

class TestGameState(unittest.TestCase):
    def test_move_character(self):
        game_state = GameState()
        pos = _find_character_position(game_state)
        new_pos, dir = _find_valid_direction(game_state, pos)
        if dir != None:
            game_state.move_character(dir)
            self.assertEqual(_find_character_position(game_state), new_pos)