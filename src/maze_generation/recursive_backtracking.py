import random
from src.constants import *
import pygame


def generate_maze(maze, start_coordinates, rects, color_map, WINDOW):
    start_x, start_y = start_coordinates

    def carve_path(x, y):
        if maze[y][x] == 'w':
            maze[y][x] = 'c'
        rect = rects[y][x]
        pygame.draw.rect(WINDOW, color_map[maze[y][x]], rect)
        pygame.display.flip()
        pygame.time.delay(50)

        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 'w':
                mx, my = x + dx // 2, y + dy // 2
                if maze[my][mx] == 'w':
                    maze[my][mx] = 'c'
                rect = rects[my][mx]
                pygame.draw.rect(WINDOW, color_map[maze[my][mx]], rect)
                pygame.display.flip()
                pygame.time.delay(50)
                carve_path(nx, ny)

    carve_path(start_x, start_y)

    return maze,  rects
