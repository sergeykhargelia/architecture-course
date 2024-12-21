import keyboard
import time
from icontroller import IController


class KeyboardHandler:
    def __init__(self, controller: IController):
        self.controller = controller

    def start(self):
        while True:
            time.sleep(0.3)
            self.controller.on_keyboard_event(keyboard.read_key())
