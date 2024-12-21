class GameController:
    def __init__(self, display, game_state):
        self._display = display
        self._game_state = game_state
        self._display.display(game_state.get_view())

    def on_keyboard_event(event):
        # TODO
        raise NotImplementedError