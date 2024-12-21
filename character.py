class Character:
    def __init__(self, inventory=None, position: tuple[int, int] = None, stats=None):
        self._inventory = inventory
        self._position = position
        self._stats = stats

    def get_position(self) -> tuple[int, int]:
        return self._position

    def change_position(self, position):
        self._position = position

    def get_inventory(self):
        return self._inventory
    
    def add_item(self, item):
        self._inventory.add_available_item(item)

    def enable_item(self, item):
        self._inventory.enable_item(item)
    
    def disable_item(self, item):
        self._inventory.disable_item(item)

    def get_view():
        # TODO
        raise NotImplementedError