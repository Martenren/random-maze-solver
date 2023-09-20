import random

def gen_walls(maze, start_x, start_y, height, width):
    # Set the starting point
    maze[start_y][start_x] = 'c'

    # Define directions for neighboring cells
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Randomized Prim's Algorithm
    walls = [(start_y + dy, start_x + dx) for dy, dx in directions]

    while walls:
        rand_wall = random.choice(walls)
        walls.remove(rand_wall)

        y, x = rand_wall
        if y <= height or x <= width:
            if maze[y][x] == 'c':
                continue

        valid_neighbors = [(y + dx, x + dy) for dx, dy in directions if 0 <= y + dx < height and 0 <= x + dy < width]
        if sum(1 for nx, ny in valid_neighbors if maze[nx][ny] == 'c') == 1:
            maze[y][x] = 'c'

            # Check if the cell is on the outer ring (except for the start and end positions)
            if y == 0 or x == 0 or y == height - 1 or x == width - 1:
                maze[y][x] = 'w'  # Set the outer ring as walls
            else:
                walls.extend(valid_neighbors)

    # Set entrance and exit
    for i in range(1, width):
        if maze[1][i] == 'c':
            start_coordinates = (1, i)
            maze[1][i] = 's'
            break

    for i in range(width - 1, 0, -1):
        if maze[height - 2][i] == 'c':
            end_coordinates = (height - 1, i)
            maze[height - 1][i] = 'e'
            break

    return maze, start_coordinates, end_coordinates
