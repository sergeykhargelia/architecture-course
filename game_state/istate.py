from util.direction import Direction

class IState:
    def __init__(self):
        pass

    def move_character(self, direction: Direction):
        pass

    def enable_item(self):
        pass

    def disable_item(self):
        pass

    def get_view(self) -> list[list[str]]:
        pass
