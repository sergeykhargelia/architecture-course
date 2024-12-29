from sshkeyboard import listen_keyboard
from icontroller import IController

class KeyboardHandler:
    def __init__(self, controller: IController):
        self.controller = controller

    # Listen keyboard events until button 'q' is pressed
    def start(self):
        listen_keyboard(
            on_press=self.controller.on_keyboard_event,
            until='q'
        )