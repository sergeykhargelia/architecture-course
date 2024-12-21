import random
from cell import Cell


def generate_position(width, height) -> tuple[int, int]:
    return random.randint(0, width - 1), random.randint(0, height - 1)


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell() for _ in range(height)] for _ in range(width)]

    def get_cell(self, position: tuple[int, int]) -> Cell:
        # todo: verify cell position
        return self.grid[position[0]][position[1]]

    def open_hidden_cell(self):
        pass

    def get_view(self) -> list[list[str]]:
        view = []
        for y in range(self.height):
            row_view = []
            for x in range(self.width):
                cell = self.grid[x][y]
                if cell.is_target:
                    row_view.append('H' if cell.is_hidden else 'T')
                    continue
                row_view.append('#' if cell.is_hidden else ' ')
            view.append(row_view)
        return view

    @classmethod
    def generate(cls, width, height, hidden_prob=0.5):
        mp = cls(width, height)

        target_position = generate_position(width, height)
        mp.grid[target_position[0]][target_position[1]].is_target = True

        for x in range(width):
            for y in range(height):
                if random.random() < hidden_prob:
                    mp.grid[x][y].is_hidden = True

        return mp
