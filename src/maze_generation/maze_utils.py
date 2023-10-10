import pygame
from src.constants import *


def draw_rect(rect, color, WINDOW):
    pygame.draw.rect(WINDOW, color, rect)
    pygame.display.flip()
    pygame.time.delay(80)


def get_cells_around(x, y, is_wall):
    frontier = []
    for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
        if 1 <= x+dx < MAZE_WIDTH-1 and 1 <= y+dy < MAZE_HEIGHT-1:
            if is_wall(x+dx, y+dy):    # is wall or is cell depending on lambda func input
                frontier.append((x+dx, y+dy))
    return frontier


def get_passage_cells(maze, x, y):
    return get_cells_around(x, y, lambda _x, _y: maze[_y][_x] == 'c' or maze[_y][_x] == 's' or maze[_y][_x] == 'e')


def get_frontier(maze, x, y):
    return get_cells_around(x, y, lambda _x, _y: maze[_y][_x] == 'w')


def connect(maze, frontier, neighbour, WINDOW, color_map, rects):
    f_x, f_y = frontier
    n_x, n_y = neighbour
    x = (frontier[0] + neighbour[0]) // 2
    y = (frontier[1] + neighbour[1]) // 2
    if maze[y][x] == 'w':
        maze[y][x] = 'c'
    if maze[f_y][f_x] == 'w':
        maze[f_y][f_x] = 'c'
    if maze[n_y][n_x] == 'w':
        maze[n_y][n_x] = 'c'

    draw_rect(rects[y][x], color_map[maze[y][x]], WINDOW)
    draw_rect(rects[f_y][f_x], color_map[maze[f_y][f_x]], WINDOW)
    draw_rect(rects[n_y][n_x], color_map[maze[n_y][n_x]], WINDOW)

