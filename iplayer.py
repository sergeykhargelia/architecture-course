class Player:
    def __init__(self, name, position, stats):
        self._name = name
        self._position = position
        self._stats = stats

    # Update the given component of character statistics
    def update_stats(self, key, delta):
        self._stats[key] += delta

    # Get character position
    def get_position(self):
        return self._position

    # Change character position
    def change_position(self, position):
        self._position = position

    def handle_attack(self, attack_pts) -> bool:
        damage = max(0, attack_pts - self._stats['defense'])
        self._stats['health'] -= damage
        return self._stats['health'] > 0
    
    def get_view(self):
        return {
            'name': self._name,
            'stats': self._stats
        }