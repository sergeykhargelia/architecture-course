from iplayer import Player
from mob_strategy import RandomMobStrategy

class Mob(Player):
    def __init__(self, name, strategy, position, stats=None):
        super().__init__(name, position, stats)
        self._strategy = strategy

    def make_move(self, character_position):
        self.change_position(self._strategy.make_move(self.get_position(), character_position))

class AffectedMob(Mob):
    def __init__(self, mob, strategy_under_affection, affection_time=5):
        super().__init__(mob._name, mob._strategy, mob._position, mob._stats)
        self._strategy_under_affection = strategy_under_affection
        self._affection_time = affection_time

    def make_move(self, character_position):
        if self._affection_time > 0:
            super().change_position(self._strategy_under_affection.make_move(super().get_position(), character_position))
            self._affection_time -= 1
        else:
            super().make_move(character_position)