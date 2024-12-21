from rich.live import Live

class Display:
    def __init__(self):
        self._live = None

    def display(self, content):
        if not self._live:
            self._live = Live(content, auto_refresh=False)
        else:
            self._live.update(content, refresh=True)