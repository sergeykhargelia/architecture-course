import unittest

from players.inventory import Inventory
from map_state.item import Item

class TestInventory(unittest.TestCase):
    def test_updates(self):
        inventory = Inventory()
        current_view = {
            'available': [],
            'enabled': []
        }
        item = Item('x', 1, 2)
        current_view['available'].append(item.get_view())
        inventory.add_available_item(item)
        self.assertEqual(inventory.get_view(), current_view)
        current_view['enabled'].append(item.get_view())
        inventory.enable_item(item)
        self.assertEqual(inventory.get_view(), current_view)
        current_view['enabled'].remove(item.get_view())
        inventory.disable_item(item)
        self.assertEqual(inventory.get_view(), current_view)
