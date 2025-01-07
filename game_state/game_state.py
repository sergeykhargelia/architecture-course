import os
import map_state
from enum import Enum, auto
from game_state.istate import IState
from util.direction import Direction, get_delta_by_direction
from players.mob import AffectedMob
from map_state.cell import CellType
from players.mob_strategy import RandomMobStrategy, MobStrategyGenerator
from map_builder import MapGenerator, MapLoader
from player_generator import SimpleCharacterGenerator, SimpleMobGenerator

class MoveResult(Enum):
    WIN = auto()
    LOSE = auto()
    IN_PROGRESS = auto()

class GameState(IState):
    def __init__(self, levels_count=5, default_height=10, default_width=10, max_visible_dist=2):
        super().__init__()
        self._levels_count = levels_count
        self._level = 1
        self._max_visible_dist = max_visible_dist
        
        self._map, self._character, self._mobs = MapGenerator(
            SimpleCharacterGenerator(), None,
            self._level, default_height, default_width,
            map_state.generate_position,
            map_state.generate_cell_type,
            map_state.generate_item
        ).build()
        
        self._open_hidden_cells()

    def _init_new_level_state(self):
        self._level += 1
        height, width = self._map.get_size()
        if self._level < self._levels_count:
            self._map, self._character, self._mobs = MapGenerator(
                SimpleCharacterGenerator(self._character),
                SimpleMobGenerator(MobStrategyGenerator()), 
                self._level, height, width,
                map_state.generate_position,
                map_state.generate_cell_type,
                map_state.generate_item
            ).build()
        else:
            self._map, self._character, self._mobs = MapLoader(
                SimpleCharacterGenerator(self._character),
                SimpleMobGenerator(MobStrategyGenerator()),
                os.path.join('assets', 'final_level_map.txt')       
            ).build()

        self._character.update_stats_after_level_up()
        self._open_hidden_cells()

    def _open_hidden_cells(self):
        character_pos = self._character.get_position()
        for delta_x in range(-self._max_visible_dist, self._max_visible_dist + 1):
            for delta_y in range(-self._max_visible_dist, self._max_visible_dist + 1):
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
                mob.make_move(self._map, old_position)
                if mob.get_position() == new_position:
                    if not self._process_battle(mob):
                        return MoveResult.LOSE
                    
                    if mob.is_alive():
                        updated_mobs.append(AffectedMob(mob, RandomMobStrategy()))
                else:
                    updated_mobs.append(mob)
                    if mob.need_replicate():
                        updated_mobs.append(mob.clone())

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