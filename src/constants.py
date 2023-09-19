from enum import Enum
import pygame


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

CELL_SIZE = 40
MARGIN = 0

WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)

MAZE_WIDTH = (WINDOW_WIDTH - MARGIN) // (CELL_SIZE + MARGIN)
MAZE_HEIGHT = (WINDOW_HEIGHT - MARGIN) // (CELL_SIZE + MARGIN)


class Colors(Enum):
    WHITE = (255, 255, 255)  # Path
    BLACK = (0, 0, 0)   # Walls
    RED = (255, 0, 0)   # End point
    GREEN = (0, 255, 0)  # Start point

