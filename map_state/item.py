import random

class Item:
    def __init__(self, name, attack_pts, defense_pts):
        self.name = name
        self.attack_pts = attack_pts
        self.defense_pts = defense_pts

    # Get string representation for item
    def get_view(self):
        return self.name

_items = [Item('dagger', 1, 0), Item('shield', 0, 1)]

# Choose random item from the given _item set
def generate_item():
    return random.choice(_items)