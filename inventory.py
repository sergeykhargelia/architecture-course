class Inventory:
    def __init__(self):
        self._available_items = []
        self._enabled_items = []

    def add_available_item(self, item):
        self._available_items.add(item)

    def enable_item(self, item):
        if item in self._available_items:
            self._enabled_items.add(item)

    def disable_item(self, item):
        if item in self._enabled_items:
            self._enabled_items.remove(item)

    def get_view(self):
        return list(map(lambda x: x.get_view(), self._enabled_items))