from enum import Enum, auto

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()

# Get (x, y) delta by direction
def get_delta_by_direction(direction: Direction) -> tuple[int, int]:
    match direction:
        case Direction.UP: return 0, -1
        case Direction.DOWN: return 0, 1
        case Direction.LEFT: return -1, 0
        case Direction.RIGHT: return 1, 0