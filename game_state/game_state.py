import random
import map_state
from enum import Enum, auto
from game_state.istate import IState
import map_state.map_state
from util.direction import Direction, get_delta_by_direction
from players.character import Character
from players.mob import Mob, AffectedMob
from map_state.cell import CellType
from players.inventory import Inventory
from players.mob_strategy import RandomMobStrategy, get_strategy_by_id

class MoveResult(Enum):
    WIN = auto()
    LOSE = auto()
    IN_PROGRESS = auto()

class GameState(IState):
    def __init__(self, levels_count=5, default_width=10, default_height=10):
        super().__init__()
        self._levels_count = levels_count
        self._level = 1
        self._map = map_state.map_state.generate_map(self._level, default_width, default_height)
        self._character = Character(
            'C',
            Inventory(),
            self._place_players()[0]
        )
        self._mobs = []
        self._open_hidden_cells()

    def _init_new_level_state(self):
        self._level += 1
        width, height = self._map.get_size()
        self._map = map_state.map_state.generate_map(self._level, width, height)
        self._init_new_level_players()

    def _init_new_level_players(self):
        positions = self._place_players()
        self._character.update_stats_after_level_up()
        self._character.change_position(positions[0])
        self._open_hidden_cells()
        
        self._mobs = []
        for i in range(1, self._level):
            name = f'mob{i}'
            strategy = (get_strategy_by_id(i - 1))(self._map)
            self._mobs.append(Mob(name, strategy, positions[i]))

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

    def _process_battle(self, mob):
        if not self._character.handle_attack(mob):
            return False
        
        if not mob.handle_attack(self._character):
            self._character.update_stats_after_kill()

        return True

    # Make a move and update game state
    def move_character(self, direction: Direction) -> MoveResult:
        delta_x, delta_y = get_delta_by_direction(direction)
        old_position = self._character.get_position()
        new_position = (old_position[0] + delta_y, old_position[1] + delta_x)
        if self._map.is_cell_exists(new_position):
            cell_type = self._map.get_cell(new_position).cell_type
            if cell_type == CellType.OBSTACLE:
                return MoveResult.IN_PROGRESS
            
            if cell_type == CellType.ITEM:
                self._character.add_item(self._map.get_cell(new_position).item)
                self._map.remove_cell_content(new_position)
            
            updated_mobs = []
            for mob in self._mobs:
                mob.make_move(old_position)
                if mob.get_position() == new_position:
                    if not self._process_battle(mob):
                        return MoveResult.LOSE
                    
                    if mob.is_alive():
                        updated_mobs.append(AffectedMob(mob, RandomMobStrategy(self._map)))
                else:
                    updated_mobs.append(mob)

            self._mobs = updated_mobs
            if cell_type == CellType.TARGET:
                if self._level == self._levels_count:
                    return MoveResult.WIN
                
                self._init_new_level_state()
            else:
                self._character.change_position(new_position)
                self._open_hidden_cells()

        return MoveResult.IN_PROGRESS

    # Enable character's item
    def enable_item(self, item):
        self._character.enable_item(item)

    # Disable character's item
    def disable_item(self, item):
        self._character.disable_item(item)

    # Get compact representation of the game state
    def get_view(self):
        map_view = self._map.get_view()
        def add_player(position, name):
            if self._map.get_cell(position).is_hidden:
                return
            
            cell = map_view['grid'][position[0]][position[1]]
            if len(cell) > 0:
                cell += ','
            
            cell += name
            map_view['grid'][position[0]][position[1]] = cell

        add_player(self._character.get_position(), self._character.get_name())
        for mob in self._mobs:
            add_player(mob.get_position(), mob.get_name())

        return {
            'map': map_view,
            'character': self._character.get_view(),
            'mobs': list(map(lambda mob: mob.get_view(), self._mobs))
        }