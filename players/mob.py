import random

from players.iplayer import Player
from players.mob_strategy import RandomMobStrategy


class Mob(Player):
    def __init__(self, name, strategy, position, stats=None, replication_prob=0.01):
        super().__init__(name, position, stats)
        self._strategy = strategy
        self._replication_prob = replication_prob

    def need_replicate(self):
        return random.random() < self._replication_prob

    def clone(self):
        return Mob(self._name, self._strategy, self._position, self._stats)            

    def make_move(self, map_state, character_position):
        self.change_position(self._strategy.make_move(map_state, self.get_position(), character_position))

class AffectedMob(Mob):
    def __init__(self, mob, strategy_under_affection, affection_time=5):
        super().__init__(mob._name, mob._strategy, mob._position, mob._stats)
        self._strategy_under_affection = strategy_under_affection
        self._affection_time = affection_time

    def clone(self):
        mob_clone = super().clone()
        return AffectedMob(mob_clone, self._strategy_under_affection, self._affection_time)

    def make_move(self, map_state, character_position):
        if self._affection_time > 0:
            super().change_position(self._strategy_under_affection.make_move(map_state, super().get_position(), character_position))
            self._affection_time -= 1
        else:
            super().make_move(map_state, character_position)