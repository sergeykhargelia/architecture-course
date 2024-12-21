from istate import IState
from direction import Direction
from map import Map, generate_position
from character import Character


class GameState(IState):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.character = Character()
        self.target_reached = False
        self.map = Map.generate(10, 10, 0.5)
        character_position = generate_position(self.map.width, self.map.height)
        self.open_hidden_cell(character_position)
        self.character.change_position(character_position)
        self.update_game_state()

    def reset_game_state(self):
        self.level += 1
        self.target_reached = False
        if self.level % 2 == 0:
            self.map = Map.load('map_example.txt')
        else:
            self.map = Map.generate(10, 10, 0.5)
        character_position = generate_position(self.map.width, self.map.height)
        self.open_hidden_cell(character_position)
        self.character.change_position(character_position)
        self.update_game_state()

    def update_game_state(self):
        character_position = self.character.get_position()
        character_cell = self.map.get_cell(character_position)
        if character_cell.is_target:
            print("Target reached you can go to next level!")
            self.target_reached = True

    def move_character(self, direction: Direction):
        delta_x = 0
        delta_y = 0
        if direction == Direction.UP:
            delta_y = -1
        elif direction == Direction.DOWN:
            delta_y = 1
        elif direction == Direction.LEFT:
            delta_x = -1
        elif direction == Direction.RIGHT:
            delta_x = 1
        old_position = self.character.get_position()
        new_position = (old_position[0] + delta_x, old_position[1] + delta_y)
        if self.check_position(new_position) and not self.open_hidden_cell(new_position):
            self.character.change_position(new_position)
            self.update_game_state()

    def check_position(self, position: tuple[int, int]) -> bool:
        return 0 <= position[0] < self.map.width and 0 <= position[1] < self.map.height

    def open_hidden_cell(self, position: tuple[int, int]) -> bool:
        cell = self.map.get_cell(position)
        if cell.is_hidden:
            cell.is_hidden = False
            return True
        return False

    def go_to_next_level(self):
        if not self.target_reached:
            return
        self.reset_game_state()

    def get_inventory(self):
        pass

    def pick_item(self):
        pass

    def enable_item(self):
        pass

    def disable_item(self):
        pass

    def get_view(self) -> list[list[str]]:
        view = self.map.get_view()
        character_position = self.character.get_position()
        view[character_position[1]][character_position[0]] = 'C'
        return view

    def generate_map(self):
        pass
