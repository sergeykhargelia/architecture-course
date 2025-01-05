from controller.icontroller import IController
from game_state.istate import IState
from util.direction import Direction

class GameController(IController):
    def __init__(self, display, game_state: IState):
        super().__init__()
        self._display = display
        self._game_state = game_state
        self._display.display(game_state.get_view())

    # React on the keyboard event: change the game state and display the changes
    def on_keyboard_event(self, key) -> bool:
        if key == 'up':
            self._game_state.move_character(Direction.UP)
        elif key == 'down':
            self._game_state.move_character(Direction.DOWN)
        elif key == 'left':
            self._game_state.move_character(Direction.LEFT)
        elif key == 'right':
            self._game_state.move_character(Direction.RIGHT)
        
        game_state_view = self._game_state.get_view()
        self._display.display(game_state_view)
        return True