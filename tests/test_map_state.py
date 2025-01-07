import unittest

from map_state.cell import Cell, CellType
from map_state.item import Item
from map_state.map_state import Map

def _get_default_map():
    return Map(3, 2, [
        [Cell(CellType.EMPTY, is_hidden=True), Cell(CellType.OBSTACLE)],
        [Cell(CellType.EMPTY), Cell(CellType.TARGET)],
        [Cell(CellType.ITEM, item=Item('a', 0, 1)), Cell(CellType.OBSTACLE)]
    ], {'level': 2})

class TestMapState(unittest.TestCase):
    def test_size(self):
        self.assertEqual(_get_default_map().get_size(), (3, 2))

    def test_get_cell(self):
        map = _get_default_map()
        self.assertEqual(map.get_cell((2, 0)).get_view(), 'a')                

    def test_cell_exists(self):
        map = _get_default_map()
        self.assertEqual(map.is_cell_exists((0, 0)), True)
        self.assertEqual(map.is_cell_exists((2, 1)), True)
        self.assertEqual(map.is_cell_exists((2, 2)), False)
        self.assertEqual(map.is_cell_exists((3, 0)), False)

    def test_cell_content_removal(self):
        map = _get_default_map()
        map.remove_cell_content((2, 0))
        self.assertEqual(map.get_cell((2, 0)).get_view(), Cell(CellType.EMPTY).get_view())

    def test_open_hidden_cell(self):
        map = _get_default_map()
        self.assertEqual(map.get_cell((0, 0)).is_hidden, True)
        map.open_hidden_cell((0, 0))
        self.assertEqual(map.get_cell((0, 0)).is_hidden, False)

    def test_view(self):
        self.assertEqual(
            _get_default_map().get_view(), 
            {
                'info': {
                    'level': 2
                },
                'grid': [
                    ['*', '#'],
                    ['', '$'],
                    ['a', '#']
                ]
            }
        )