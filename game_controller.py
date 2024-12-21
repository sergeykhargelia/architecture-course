from icontroller import IController
from istate import IState
from direction import Direction


class GameController(IController):
    def __init__(self, display, game_state: IState):
        super().__init__()
        self._display = display
        self._game_state = game_state
        self._display.display(game_state.get_view())

    def on_keyboard_event(self, key) -> bool:
        if key == 'w':
            self._game_state.move_character(Direction.UP)
        elif key == 's':
            self._game_state.move_character(Direction.DOWN)
        elif key == 'a':
            self._game_state.move_character(Direction.LEFT)
        elif key == 'd':
            self._game_state.move_character(Direction.RIGHT)
        elif key == 'n':
            print('Going to next level')
            self._game_state.go_to_next_level()
        elif key == 'q':
            print('Quit')
            return False
        game_state_view = self._game_state.get_view()
        print('\n'.join([''.join(row_view) for row_view in game_state_view]))
        return True
