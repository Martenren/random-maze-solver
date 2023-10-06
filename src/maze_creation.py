import random
import prim_algo_gen as pag
from constants import *
import time
from utils import *
import pygame


def maze_generation():
    pygame.display.set_caption("Random maze solver")

    print(MAZE_WIDTH, MAZE_HEIGHT)

    start_x = int(random.random() * MAZE_WIDTH)
    start_y = int(random.random() * MAZE_HEIGHT)

    print(start_x, start_y)

    # Initialize the maze as a grid of walls
    maze = [['w'] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]
    # print("before algo len maze: ", len(maze), len(maze[0]))

    start_time = time.time()

    maze, start_coordinates, end_coordinantes = pag.gen_walls(maze, start_x, start_y, MAZE_HEIGHT, MAZE_WIDTH)

    print("maze_generation took", time.time() - start_time, "seconds")

    return maze, start_coordinates, end_coordinantes