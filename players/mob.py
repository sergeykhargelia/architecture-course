import random

from players.iplayer import Player
from players.mob_state import *

class Mob(Player):
    def __init__(self, name, strategy, position, state=MobRegularState(), stats=None, replication_prob=0.01):
        super().__init__(name, position, stats)
        self._strategy = strategy
        self.state = state
        self._replication_prob = replication_prob

    def get_strategy(self):
        return self._strategy

    def need_replicate(self):
        return random.random() < self._replication_prob

    def update_stats(self, key, delta):
        super().update_stats(key, delta)
        self.state.on_stats_update(self, key, delta)

    def clone(self):
        return Mob(self._name, self._strategy, self._position, self.state, self._stats, self._replication_prob)            

    def make_move(self, map_state, character_position):
        self.state.make_move(map_state, self, character_position)