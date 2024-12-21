from direction import Direction


class IState:
    def __init__(self):
        pass

    def move_character(self, direction: Direction):
        pass

    def open_hidden_cell(self, position: tuple[int, int]) -> bool:
        pass

    def go_to_next_level(self):
        pass

    def get_inventory(self):
        pass

    def pick_item(self):
        pass

    def enable_item(self):
        pass

    def disable_item(self):
        pass

    def get_view(self) -> list[list[str]]:
        pass
