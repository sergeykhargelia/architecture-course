import random
from typing import List
from map_state import Map
from character import Character
from mob import Mob
from cell import Cell, CellType

class IMapBuilder:
    def __init__(self, character_generator, mob_generator):
        self._character_generator = character_generator
        self._mob_generator = mob_generator

    def _get_player_positions(self):
        pass

    def _get_map_state(self):
        pass

    def set_character_generator(self, character_generator):
        self._character_generator = character_generator
        return self

    def set_mob_generator(self, mob_generator):
        self._mob_generator = mob_generator
        return self
    
    def build(self) -> tuple[Map, Character, List[Mob]]:
        map_state = self._get_map_state()
        positions = self._get_player_positions()
        character = self._character_generator.generate_character(positions[0])
        mobs = []
        for id, position in enumerate(positions[1:]):
            mobs.append(self._mob_generator.generate_mob(position, id))
        return map_state, character, mobs

class MapLoader(IMapBuilder):
    def __init__(self, character_generator, mob_generator, filename):
        super().__init__(character_generator, mob_generator)
        self._filename = filename
        self._map_state, self._player_positions = self._read_map_from_file()

    def _get_player_positions(self):
        return self._player_positions
    
    def _get_map_state(self):
        return self._map_state

    def _read_map_from_file(self):
        with open(self._filename) as f:
            height, width, level = map(int, f.readline().split())
            player_positions = [None] * level
            grid = []

            for i in range(height):
                row = []
                for j, str in enumerate(f.readline().split()):
                    if str.startswith('mob'):
                        player_positions[int(str.removeprefix('mob'))] = (i, j)
                    elif str == 'C':
                        player_positions[0] = (i, j)

                    match str:
                        case '#': cell = Cell(CellType.OBSTACLE, is_hidden=True)
                        case '$': cell = Cell(CellType.TARGET, is_hidden=True)
                        case _: cell = Cell(CellType.EMPTY, is_hidden=True)

                    row.append(cell)

                grid.append(row)

            return Map(height, width, grid, {'level': level}), player_positions


class MapGenerator(IMapBuilder):
    def __init__(
        self, character_generator, mob_generator,
        level, height, width, 
        target_position_generator=None, 
        cell_type_generator=None,
        item_generator=None,
        map_info={}
    ):
        super().__init__(character_generator, mob_generator)
        self._height = height
        self._width = width
        self._level = level
        self._target_position_generator = target_position_generator
        self._cell_type_generator = cell_type_generator
        self._item_generator = item_generator
        self._map_info = map_info
        self._map_state = self._generate_map()
        self._player_positions = self._generate_player_positions()

    def set_target_position_generator(self, target_position_generator):
        self._target_position_generator = target_position_generator
        return self
    
    def set_cell_type_generator(self, cell_type_generator):
        self._cell_type_generator = cell_type_generator
        return self

    def set_item_generator(self, item_generator):
        self._item_generator = item_generator
        return self

    def _get_player_positions(self):
        return self._player_positions
    
    def _get_map_state(self):
        return self._map_state

    def _generate_map(self):
        self._map_info['level'] = self._level
        grid = []
        target_position = self._target_position_generator(self._height, self._width)
        
        for x in range(self._height):
            row = []
            for y in range(self._width):
                if (x, y) == target_position:
                    row.append(Cell(CellType.TARGET, is_hidden=True))
                else:
                    cell_type = self._cell_type_generator(self._level)
                    if cell_type == CellType.ITEM:
                        row.append(Cell(CellType.ITEM, self._item_generator(), True))
                    else:
                        row.append(Cell(cell_type, is_hidden=True))

            grid.append(row)

        return Map(self._height, self._width, grid, self._map_info)

    def _generate_player_positions(self):
        empty_cells_coordinates = []
        for x in range(self._height):
            for y in range(self._width):
                position = (x, y)
                cell = self._map_state.get_cell(position)
                if cell.cell_type == CellType.EMPTY:
                    empty_cells_coordinates.append(position)

        random.shuffle(empty_cells_coordinates)
        return empty_cells_coordinates[:self._level]