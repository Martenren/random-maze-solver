# import random
#
# def gen_walls(maze, start_x, start_y, height, width):
#     # Set the starting point
#     maze[start_y][start_x] = 'c'
#
#     # Define directions for neighboring cells
#     directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
#
#     # Randomized Prim's Algorithm
#     walls = [(start_y + dy, start_x + dx) for dy, dx in directions]
#
#     while walls:
#         rand_wall = random.choice(walls)
#         walls.remove(rand_wall)
#
#         y, x = rand_wall
#
#         if y < height and x < width:
#             if maze[y][x] == 'c':
#                 continue
#
#             valid_neighbors = [(y + dy, x + dx) for dy, dx in directions if 0 <= y + dy < height and 0 <= x + dx < width]
#             if sum(1 for ny, nx in valid_neighbors if maze[ny][nx] == 'c') == 1:
#                 maze[y][x] = 'c'
#
#                 # Check if the cell is on the outer ring (except for the start and end positions)
#                 if y == 0 or x == 0 or y == height - 1 or x == width - 1:
#                     # Do not mark as 'w' here, mark as 'c' and update after maze generation
#                     pass
#                 else:
#                     walls.extend(valid_neighbors)
#
#     # Determine valid exit locations that are not in a corner
#     valid_exit_locations = [(1, i) for i in range(1, width - 1)]
#
#     # Randomly select an exit location from the valid ones
#     exit_coordinates = random.choice(valid_exit_locations)
#     end_coordinates = (height - 1, exit_coordinates[1])
#
#     # Set start and exit
#     maze[1][exit_coordinates[1]] = 's'
#     maze[end_coordinates[0]][end_coordinates[1]] = 'e'
#
#     # Mark the outer ring cells as 'w'
#     for y in range(height):
#         for x in range(width):
#             if y == 0 or x == 0 or y == height - 1 or x == width - 1:
#                 if maze[y][x] == 'c':
#                     maze[y][x] = 'w'
#
#     return maze, (1, exit_coordinates[1]), end_coordinates

import random

def generate_maze(height, width):
    maze = [['w' for _ in range(width)] for _ in range(height)]

    def carve_path(x, y):
        maze[y][x] = 'c'

        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 'w':
                mx, my = x + dx // 2, y + dy // 2
                maze[my][mx] = 'c'
                carve_path(nx, ny)

    # Start carving from a random point
    start_x = random.randrange(1, width, 2)
    start_y = random.randrange(1, height, 2)
    carve_path(start_x, start_y)

    # Set the start and exit
    maze[1][1] = 's'
    maze[height - 2][width - 1] = 'e'

    return maze, (1, 1), (height-1, width-1)

