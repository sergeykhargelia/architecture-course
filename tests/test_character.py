import unittest

from players.character import Character
from players.inventory import Inventory

def _get_default_character():
    return Character('Bob', Inventory(), (0, 0), {'health': 5, 'attack': 3, 'defense': 1})

class TestCharacter(unittest.TestCase):
    def test_position(self):
        character = _get_default_character()
        self.assertEqual(character.get_position(), (0, 0))
        character.change_position((1, 2))
        self.assertEqual(character.get_position(), (1, 2))

    def test_view(self):
        character = _get_default_character()
        current_view = {
            'name': 'Bob',
            'stats': {
                'health':  5,
                'attack':  3,
                'defense': 1
            },
            'inventory': {
                'available': [],
                'enabled': []
            }
        }

        self.assertEqual(character.get_view(), current_view)
    
    def test_stats(self):
        character = _get_default_character()
        current_stats = {
            'health':  5,
            'attack':  3,
            'defense': 1
        }
        
        def get_stats():
            return character.get_view()['stats']
        
        self.assertEqual(get_stats(), current_stats)
        character.update_stats('health', -1)
        current_stats['health'] -= 1
        self.assertEqual(get_stats(), current_stats)
        character.handle_attack(_get_default_character())
        current_stats['health'] -= 2 # because we have one point of defense
        self.assertEqual(get_stats(), current_stats)
