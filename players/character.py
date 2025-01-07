from players.iplayer import Player

class Character(Player):
    def __init__(self, name, inventory, position, stats=None):
        if stats is None:
            stats = {'health': 5, 'experience': 0, 'attack': 1, 'defense': 0}

        super().__init__(name, position, stats)
        self._inventory = inventory
        self._level = 1
        
    # Get character's inventory
    def get_inventory(self):
        return self._inventory

    # Add item to the character's inventory
    def add_item(self, item):
        self._stats['attack'] += item.attack_pts
        self._stats['defense'] += item.defense_pts
        self._inventory.add_available_item(item)

    # Enable the given item from the character's inventory        
    def enable_item(self, item):
        self._inventory.enable_item(item)

    # Disable the given item from the character's inventory
    def disable_item(self, item):
        self._inventory.disable_item(item)

    def _update_character_level(self):
        current_level = super().get_stats()['experience'] // 10
        if self._level < current_level:
            super().update_stats('attack', current_level - self._level)
            super().update_stats('defense', current_level - self._level)
            self._level = current_level

    # Obtain bonus for killing the mob
    def update_stats_after_kill(self):
        super().update_stats('experience', 1)
        self._update_character_level()

    # Obtain bonus for the level-up
    def update_stats_after_level_up(self):
        super().update_stats('experience', 2)
        self._update_character_level()
    
    def clone(self):
        return Character(self._name, self._inventory, self._position, self._stats)

    # Get a compact representation of the character 
    def get_view(self):
        view = super().get_view()
        view['inventory'] = self._inventory.get_view()
        return view