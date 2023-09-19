import sys
from particle import particle_creation
from utils import *


class Game:
    def __init__(self, maze, start_coordinates, end_coordinantes):
        self.maze = maze
        self.start_coordinates = start_coordinates
        self.end_coordinantes = end_coordinantes

    def start(self):
        running = True
        particles = particle_creation(self.start_coordinates, 20, 20,
                                      0, 0, 1)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Handle mouse click events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:  # Left mouse button
                        mouse_x, mouse_y = pygame.mouse.get_pos()

                        cell_x = pixel_to_cell(mouse_x)
                        cell_y = pixel_to_cell(mouse_y)

                        # Check if the clicked cell is within the maze bounds
                        if 0 <= cell_x < MAZE_WIDTH and 0 <= cell_y < MAZE_HEIGHT:
                            # Check if clicked cell is not the start or end point
                            if self.maze[cell_y][cell_x] not in ['e', 's']:
                                self.maze[cell_y][cell_x] = 'w' if self.maze[cell_y][cell_x] == 'c' else 'c'

            # Clear the screen
            WINDOW.fill(Colors.WHITE.value)

            # Draw the maze
            for row in range(MAZE_HEIGHT):
                for col in range(MAZE_WIDTH):
                    if self.maze[row][col] == 'c':
                        color = Colors.WHITE.value
                    elif self.maze[row][col] == 'w':
                        color = Colors.BLACK.value
                    elif self.maze[row][col] == 'e':
                        color = Colors.RED.value
                    else:
                        color = Colors.GREEN.value
                    pygame.draw.rect(
                        WINDOW,
                        color,
                        [(MARGIN + CELL_SIZE) * col + MARGIN, (MARGIN + CELL_SIZE) * row + MARGIN, CELL_SIZE,
                         CELL_SIZE],
                    )

            for particle in particles:
                cell_x = pixel_to_cell(particle.x)
                cell_y = pixel_to_cell(particle.y)
                print(cell_x, cell_y)
                if self.maze[cell_y][cell_x] == "e":
                    running = False

                particle.move_vertical()
                particle.move_horizontal()

                particle.handle_collision(self.maze, MARGIN, CELL_SIZE, WINDOW, MAZE_WIDTH, MAZE_HEIGHT)

                particle.draw(WINDOW)

            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()
        sys.exit()
