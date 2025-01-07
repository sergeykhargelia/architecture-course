import unittest

from players.mob import Mob
from map_state.map_state import Map
from map_state.cell import Cell, CellType
from players.mob_strategy import *

def _get_simple_1d_map():
    return Map(1, 3, [[Cell(CellType.EMPTY) for _ in range(3)]])

class TestMob(unittest.TestCase):
    def test_deterministic_mobs(self):
        for strategy, expected_pos in [
            (PassiveMobStrategy, (0, 1)), 
            (AggressiveMobStrategy, (0, 0))
        ]:
            with self.subTest():
                mob = Mob('mob', strategy(_get_simple_1d_map()), (0, 1))
                mob.make_move((0, 0))
                self.assertEqual(mob.get_position(), expected_pos)

    def test_undeterministic_mob(self):
        possible_positions = set()
        for i in range(20):
            mob = Mob('mob', RandomMobStrategy(_get_simple_1d_map()), (0, 1))
            mob.make_move((0, 0))
            possible_positions.add(mob.get_position())

        self.assertEqual(len(possible_positions), 3)