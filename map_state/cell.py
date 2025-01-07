import random
from enum import Enum, auto

class CellType(Enum):
    EMPTY = auto()
    OBSTACLE = auto()
    TARGET = auto()
    ITEM = auto()

# Generate random cell type. 
# Number of empty cells decreases with each level.
def generate_cell_type(level):
    empty_prob = 1 - 0.05 * level
    item_prob = 0.01

    x = random.random()
    if x < empty_prob:
        return CellType.EMPTY
    elif x  < empty_prob + item_prob:
        return CellType.ITEM
    else:
        return CellType.OBSTACLE

class Cell:
    def __init__(self, cell_type, item=None, is_hidden=False):
        self.cell_type = cell_type
        self.item = item
        self.is_hidden = is_hidden

    # Get string representation of cell
    def get_view(self):
        if self.is_hidden:
           return '*'

        match self.cell_type:
            case CellType.EMPTY: return ''
            case CellType.OBSTACLE: return '#'
            case CellType.TARGET: return '$'
            case CellType.ITEM: return self.item.get_view()
            case _: raise ValueError('Unknown cell type')