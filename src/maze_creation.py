import src.maze_generation.prim as prim
import src.maze_generation.kruskal as kruskal
import src.maze_generation.recursive_backtracking as recursive_backtracking
import src.maze_generation.wilson as wilson
import src.maze_generation.aldous_broder as aldous_broder
from utils import *
import pygame


def maze_generation(WINDOW, maze_algorithm):
    pygame.display.set_caption("Random maze solver")

    # start_time = time.time()

    color_map = {
        'c': Colors.WHITE.value,
        'w': Colors.BLACK.value,
        'e': Colors.RED.value,
        's': Colors.GREEN.value,
    }

    maze = [['w' for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]
    rects = []

    for row in range(MAZE_HEIGHT):
        rects.append([])
        for col in range(MAZE_WIDTH):
            rect = pygame.rect.Rect(
                (MARGIN + CELL_SIZE) * col + MARGIN,
                (MARGIN + CELL_SIZE) * row + MARGIN,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(WINDOW, color_map['w'], rect)
            rects[-1].append(rect)

    pygame.display.flip()
    pygame.time.delay(100)

    start_coordinates = (random.randrange(1, MAZE_WIDTH//2, 2), random.randrange(1, MAZE_HEIGHT//2, 2))
    start_x, start_y = start_coordinates

    end_coordinates = (MAZE_WIDTH - 1, MAZE_HEIGHT - 2)

    # Set the start and exit
    maze[start_y][start_x] = 's'
    maze[MAZE_HEIGHT - 2][MAZE_WIDTH - 1] = 'e'

    rect = rects[start_y][start_x]
    pygame.draw.rect(WINDOW, color_map['s'], rect)

    rect = rects[MAZE_HEIGHT - 2][MAZE_WIDTH - 1]
    pygame.draw.rect(WINDOW, color_map['e'], rect)

    if maze_algorithm == "prim":
        maze, rects = prim.generate_maze(maze, start_coordinates, rects, color_map, WINDOW)
    elif maze_algorithm == "kruskal":
        maze, rects = kruskal.generate_maze(maze, start_coordinates, rects, color_map, WINDOW)
    elif maze_algorithm == "recursive_backtracking":
        maze, rects = recursive_backtracking.generate_maze(maze, start_coordinates, rects, color_map, WINDOW)
    elif maze_algorithm == "wilson":
        maze, rects = wilson.generate_maze(maze, start_coordinates, rects, color_map, WINDOW)
    elif maze_algorithm == "aldous_broder":
        maze, rects = aldous_broder.generate_maze(maze, start_coordinates, rects, color_map, WINDOW)
    else:
        print("Invalid maze generation algorithm entered.")
        exit()

    rects = [rect for row in rects for rect in row]

    cell_colors = [color_map[cell] for row in maze for cell in row]

    return maze, start_coordinates, end_coordinates, cell_colors, rects
