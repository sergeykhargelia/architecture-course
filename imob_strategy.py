from map_state import Map
from cell import CellType

class IMobStrategy():
    def __init__(self, map_state: Map):
        self._map_state = map_state
    
    def _get_allowed_neighbours(self, position: tuple[int, int]):
        result = [position]
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_position = (position[0] + dx, position[1] + dy)
            if self._map_state.is_cell_exists(new_position) and self._map_state.get_cell(new_position).cell_type != CellType.OBSTACLE:
                result.append(new_position)

        return result

    # Calculate new position of mob by its current position and position of character
    def make_move(self, mob_position: tuple[int, int], character_position: tuple[int, int]) -> tuple[int, int]:
        pass