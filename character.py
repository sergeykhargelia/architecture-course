from iplayer import Player

class Character(Player):
    def __init__(self, name, inventory, position, stats):
        super().__init__(name, position, stats)
        self._inventory = inventory
        
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

    # Get a compact representation of the character 
    def get_view(self):
        view = super().get_view()
        view['inventory'] = self._inventory.get_view()
        return view