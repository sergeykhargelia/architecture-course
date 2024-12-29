import random
import map_state
from istate import IState
from direction import Direction
from character import Character
from cell import CellType
from inventory import Inventory

class GameState(IState):
    def __init__(self, default_width=10, default_height=10):
        super().__init__()
        self._level = 1
        self._map = map_state.generate_map(self._level, default_width, default_height, {})
        self._character = Character(
            'C', 
            Inventory(), 
            self._place_players()[0], 
            {'health': 5, 'experience': 0, 'attack': 1, 'defense': 0}
        )
        self._mobs = []
        self._open_hidden_cells()

    def _init_new_level_state(self):
        self._level += 1
        width, height = self._map.get_size()
        self._map = map_state.generate_map(self._level, width, height, {})
        self._init_new_level_players()

    def _init_new_level_players(self):
        positions = self._place_players()
        self._character.update_stats('experience', 1)
        self._character.change_position(positions[0])
        self._open_hidden_cells()

    def _place_players(self):
        empty_cells_coordinates = []
        width, height = self._map.get_size()
        for x in range(width):
            for y in range(height):
                position = (x, y)
                cell = self._map.get_cell(position)
                if cell.cell_type == CellType.EMPTY:
                    empty_cells_coordinates.append(position)

        random.shuffle(empty_cells_coordinates)
        return empty_cells_coordinates[:self._level]        

    def _open_hidden_cells(self):
        character_pos = self._character.get_position()
        max_dist = 2

        for delta_x in range(-max_dist, max_dist + 1):
            for delta_y in range(-max_dist, max_dist + 1):
                pos = (character_pos[0] + delta_x, character_pos[1] + delta_y)
                if self._map.is_cell_exists(pos):
                    self._map.open_hidden_cell(pos)

    # Make a move and update game state
    def move_character(self, direction: Direction):
        delta_x = 0
        delta_y = 0
        match direction:
            case Direction.UP:
                delta_y = -1
            case Direction.DOWN:
                delta_y = 1
            case Direction.LEFT:
                delta_x = -1
            case Direction.RIGHT:
                delta_x = 1
        
        old_position = self._character.get_position()
        new_position = (old_position[0] + delta_y, old_position[1] + delta_x)
        if self._map.is_cell_exists(new_position):
            cell_type = self._map.get_cell(new_position).cell_type
            if cell_type == CellType.TARGET:
                self._init_new_level_state()
                return
            elif cell_type != CellType.OBSTACLE:
                if cell_type == CellType.ITEM:
                    self._character.add_item(self._map.get_cell(new_position).item)
                    self._map.remove_cell_content(new_position)

                self._character.change_position(new_position)
                self._open_hidden_cells()

    def enable_item(self):
        pass

    def disable_item(self):
        pass

    # Get compact representation of the game state
    def get_view(self):
        map_view = self._map.get_view()
        character_position = self._character.get_position()
        map_view['grid'][character_position[0]][character_position[1]] = self._character.get_view()['name']

        for mob in self._mobs:
            pos = mob.get_position()
            map_view['grid'][pos[0]][pos[1]] = mob.get_view()['name']

        return {
            'map': map_view,
            'character': self._character.get_view(),
            'mobs': list(map(lambda mob: mob.get_view(), self._mobs))
        }