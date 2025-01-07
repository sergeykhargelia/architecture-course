import unittest
import os
from game_state.map_builder import MapLoader
from players.player_generator import SimpleCharacterGenerator, SimpleMobGenerator
from players.mob_strategy import MobStrategyGenerator

class TestMapBuilder(unittest.TestCase):
    def test_load_from_file(self):
        filename = os.path.join('tests', 'assets', 'small_map.txt')
        map, character, mobs = MapLoader(
            SimpleCharacterGenerator(), 
            SimpleMobGenerator(MobStrategyGenerator()), 
            filename
        ).build()
        
        self.assertEqual(len(mobs), 1)
        self.assertEqual(character.get_position(), (0, 0))
        self.assertEqual(mobs[0].get_position(), (0, 1))
        self.assertEqual(mobs[0].get_name(), 'mob1')
        
        self.assertEqual(map.get_view(), {
            'info': {
                'level': 2
            },
            'grid': [
                ['*', '*', '*'],
                ['*', '*', '*']
            ]
        })

        height, width = map.get_size()
        for i in range(height):
            for j in range(width):
                map.open_hidden_cell((i, j))

        self.assertEqual(map.get_view(), {
            'info': {
                'level': 2
            },
            'grid': [
                ['', '', '#'],
                ['', 'dagger', '$']
            ]
        })
