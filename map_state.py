import random
from cell import Cell, CellType, generate_cell_type
from item import generate_item

class Map:
    def __init__(self, width, height, grid, map_info=None):
        self._width = width
        self._height = height
        self._grid = grid
        self._info = map_info

    def _ensure_cell_exists(self, position):
        if not self.is_cell_exists(position):
            raise ValueError(f'Cell does not exist: ({position[0]}, {position[1]})')
    
    # Check that cell with the given coordinates is inside the map
    def is_cell_exists(self, position):
        return position[0] >= 0 and position[0] < self._width and \
               position[1] >= 0 and position[1] < self._height

    # Get cell by its coordinates
    def get_cell(self, position):
        self._ensure_cell_exists(position)        
        return self._grid[position[0]][position[1]]

    # Make cell with the given coordinates empty.
    # Usually because its item is taken by some player.
    def remove_cell_content(self, position):
        self._ensure_cell_exists(position)
        self._grid[position[0]][position[1]] = Cell(CellType.EMPTY)

    # Make cell with the given coordinates visible 
    def open_hidden_cell(self, position):
        self._ensure_cell_exists(position)
        self._grid[position[0]][position[1]].is_hidden = False

    # Get dimensions of the map
    def get_size(self):
        return (self._width, self._height)

    # Get map representation
    def get_view(self):
        return {
            'info': self._info,
            'grid': [list(map(lambda cell: cell.get_view(), self._grid[x])) for x in range(self._width)]
        }

# Load map from the given file    
def load_map(filename):
    # TODO
    raise NotImplementedError()

# Generate a random position on the map with given dimensions
def generate_position(width, height):
    return random.randint(0, width - 1), random.randint(0, height - 1)

# Generate random map by level and dimensions
def generate_map(level, width, height, map_info):
    map_info['level'] = level
    grid = []
    target_position = generate_position(width, height)
    
    for x in range(width):
        row = []
        for y in range(height):
            if (x, y) == target_position:
                row.append(Cell(CellType.TARGET, is_hidden=True))
            else:
                cell_type = generate_cell_type(level)
                if cell_type == CellType.ITEM:
                    row.append(Cell(CellType.ITEM, generate_item(), True))
                else:
                    row.append(Cell(cell_type, is_hidden=True))

        grid.append(row)

    return Map(width, height, grid, map_info)
