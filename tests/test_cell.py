import unittest

from map_state.cell import Cell, CellType
from map_state.item import Item

class TestCell(unittest.TestCase):
    def test_view_empty(self):
        self.assertEqual(Cell(CellType.EMPTY).get_view(), '')

    def test_view_obstacle(self):
        self.assertEqual(Cell(CellType.OBSTACLE).get_view(), '#')

    def test_view_target(self):
        self.assertEqual(Cell(CellType.TARGET).get_view(), '$')

    def test_view_item(self):
        item = Item('a', 0, 0)
        self.assertEqual(Cell(CellType.ITEM, item).get_view(), item.get_view())

    def test_view_hidden(self):
        self.assertEqual(Cell(CellType.EMPTY, is_hidden=True).get_view(), '*')
        self.assertEqual(Cell(CellType.ITEM, is_hidden=True).get_view(), '*')

    