import random
from src.maze_generation.maze_utils import *


def generate_maze(maze, start_coordinates, rects, color_map, WINDOW):
    start_x, start_y = start_coordinates

    frontier = get_frontier(maze, start_x, start_y)
    # for x, y in frontier:
    #     draw_rect(rects[y][x], Colors.GOLD.value, WINDOW)

    while frontier:
        frontier_cell = random.choice(frontier)
        frontier_neighbours = get_passage_cells(maze, frontier_cell[0], frontier_cell[1])

        if frontier_neighbours:
            neighbour = random.choice(frontier_neighbours)
            connect(maze, frontier_cell, neighbour, WINDOW, color_map, rects)

        for cell in get_frontier(maze, frontier_cell[0], frontier_cell[1]):
            frontier.append(cell)

        frontier.remove(frontier_cell)

    return maze,  rects
