import random

class Player:
    def __init__(self, name, position, stats=None):
        self._name = name
        self._position = position

        if stats is None:
            self._stats = {
                'health': random.randint(1, 2), 
                'attack': random.randint(1, 2), 
                'defense': random.randint(0, 1)
            }
        else:
            self._stats = stats

    # Update the given component of player's statistics
    def update_stats(self, key, delta):
        self._stats[key] += delta

    # Get player's statistics
    def get_stats(self):
        return self._stats

    # Check whether player is still alive
    def is_alive(self):
        return self._stats['health'] > 0

    # Get player position
    def get_position(self):
        return self._position

    # Change player position
    def change_position(self, position):
        self._position = position

    # Get player name
    def get_name(self):
        return self._name

    # Handle attack by other player
    def handle_attack(self, player) -> bool:
        attack_pts = player.get_stats()['attack']
        damage = max(0, attack_pts - self._stats['defense'])
        self._stats['health'] -= damage
        return self._stats['health'] > 0
    
    def get_view(self):
        return {
            'name': self._name,
            'stats': self._stats
        }