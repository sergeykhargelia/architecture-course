from display.display import RoguelikeConsoleDisplay
from game_state.game_state import GameState
from controller.game_controller import GameController
from keyboard_handler import KeyboardHandler
from rich.live import Live

with Live(None, auto_refresh=False) as live:
    game_state = GameState()
    controller = GameController(RoguelikeConsoleDisplay(live), game_state)
    KeyboardHandler(controller).start()