from enum import Enum


# window_size = int(input("Enter window size (square so only one value):"))

WINDOW_WIDTH = 300
WINDOW_HEIGHT = 300

CELL_SIZE = (WINDOW_HEIGHT + WINDOW_WIDTH) // 2 // 15
MARGIN = 0

WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

MAZE_WIDTH = (WINDOW_WIDTH - MARGIN) // (CELL_SIZE + MARGIN)
MAZE_HEIGHT = (WINDOW_HEIGHT - MARGIN) // (CELL_SIZE + MARGIN)


class Colors(Enum):
    WHITE = "#FFFFFF"  # Path
    BLACK = "#000000"  # Walls
    RED = "#FF0000"  # End point
    GREEN = "#00FF00"  # Start point

    # Players
    CYAN = "#00FFFF"
    BLUE = "#0000FF"
    YELLOW = "#FFFF00"
    PURPLE = "#FF00FF"
    ORANGE = "#FFA500"
    GREY = "#808080"
    PINK = "#FFC0CB"
    BROWN = "#A52A2A"
    LIME = "#008000"
    MAROON = "#800000"
    NAVY = "#000080"
    TEAL = "#008080"
    OLIVE = "#808000"
    GOLD = "#FFD700"
    INDIGO = "#4B0082"
    VIOLET = "#EE82EE"
    TURQUOISE = "#40E0D0"
    SILVER = "#C0C0C0"
    CRIMSON = "#DC143C"


