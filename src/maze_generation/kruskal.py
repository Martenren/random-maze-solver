import random
from src.maze_generation.maze_utils import *
from src.constants import *
import time


def find_set(cell, grid):
    for s in grid:
        if cell in s:
            return s


def union_sets(set1, set2, grid):
    grid.remove(set1)
    grid.remove(set2)
    grid.append(set1.union(set2))


def generate_maze(maze, start_coordinates, rects, color_map, WINDOW):
    start_x, start_y = start_coordinates

    # create set for each cell:
    grid = []

    for y in range(1, MAZE_HEIGHT-1):
        for x in range(1, MAZE_WIDTH-1):
            grid.append({(x, y)})

    frontier = get_frontier(maze, start_x, start_y)

    while frontier:
        frontier_cell = random.choice(frontier)
        frontier_neighbours = get_passage_cells(maze, frontier_cell[0], frontier_cell[1])

        if frontier_neighbours:
            neighbour = random.choice(frontier_neighbours)
            if find_set(frontier_cell, grid) != find_set(neighbour, grid):
                connect(maze, frontier_cell, neighbour, WINDOW, color_map, rects)
                union_sets(find_set(frontier_cell, grid), find_set(neighbour, grid), grid)

        for cell in get_frontier(maze, frontier_cell[0], frontier_cell[1]):
            frontier.append(cell)

        frontier.remove(frontier_cell)

    return maze, rects
