from players.mob_strategy import RandomMobStrategy

def _get_health(player):
    return player.get_stats()['health']

class IMobState:
    def make_move(self, map_state, mob, character_position):
        pass

    def on_stats_update(self, mob, key, delta):
        pass

class MobRegularState(IMobState):
    def __init__(self, critical_health_threshold=1):
        self._critical_health_threshold = critical_health_threshold
    
    def make_move(self, map_state, mob, character_position):
        mob.change_position(mob.get_strategy().make_move(
            map_state, mob.get_position(), character_position)
        )

    def on_stats_update(self, mob, key, delta):
        if _get_health(mob) <= self._critical_health_threshold:
            mob.state = MobPanicState(self._critical_health_threshold)
        elif key == 'health' and delta < 0:
            mob.state = MobAffectedState(self._critical_health_threshold, RandomMobStrategy())

class MobPanicState(IMobState):
    def __init__(self, critical_health_threshold):
        self._critical_health_threshold = critical_health_threshold

    def on_stats_update(self, mob, key, delta):
        if _get_health(mob) > self._critical_health_threshold:
            mob.state = MobRegularState(self._critical_health_threshold)

class MobAffectedState(IMobState):
    def __init__(self, critical_health_threshold, strategy_under_affection, affection_time=5):
        self._critical_health_threshold = critical_health_threshold
        self._strategy_under_affection = strategy_under_affection
        self._affection_time = affection_time

    def make_move(self, map_state, mob, character_position):
        if self._affection_time <= 0:
            if _get_health(mob) <= self._critical_health_threshold:
                mob.state = MobPanicState(self._critical_health_threshold)
            else:
                mob.state = MobRegularState(self._critical_health_threshold)
            
            mob.state.make_move(map_state, mob, character_position)

        mob.change_position(self._strategy_under_affection.make_move(map_state, mob.get_position(), character_position))
        self._affection_time -= 1
        
