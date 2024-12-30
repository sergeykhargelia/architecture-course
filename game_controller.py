from icontroller import IController
from istate import IState
from direction import Direction
from game_state import MoveResult

class GameController(IController):
    def __init__(self, display, game_state: IState):
        super().__init__()
        self._display = display
        self._game_state = game_state
        self._display.display_game_state(game_state.get_view())
        self._game_finished = False

    # React on the keyboard event: change the game state and display the changes
    def on_keyboard_event(self, key) -> bool:
        if self._game_finished:
            return
        
        match key:
            case 'up': result = self._game_state.move_character(Direction.UP)
            case 'down': result = self._game_state.move_character(Direction.DOWN)
            case 'left': result = self._game_state.move_character(Direction.LEFT)
            case 'right': result = self._game_state.move_character(Direction.RIGHT)

        match result:
            case MoveResult.WIN: self._display.display_win()
            case MoveResult.LOSE: self._display.display_lose()
            case MoveResult.IN_PROGRESS: self._display.display_game_state(self._game_state.get_view())
        
        self._game_finished = (result != MoveResult.IN_PROGRESS)