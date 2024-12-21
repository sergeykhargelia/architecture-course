from display import Display
from game_state import GameState
from game_controller import GameController
from keyboard_handler import KeyboardHandler


game_state = GameState()
controller = GameController(Display(), game_state)
keyboard_handler = KeyboardHandler(controller)
keyboard_handler.start()
