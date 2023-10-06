import sys
from particle import ParticleCluster
from utils import *
import multiprocessing
import pygame


class Game:
    def __init__(self, WINDOW, maze, start_coordinates, end_coordinantes, player_color, num_particles):
        pygame.init()
        self.WINDOW = WINDOW
        self.maze = maze
        self.start_coordinates = start_coordinates
        self.end_coordinantes = end_coordinantes
        self.clock = pygame.time.Clock()
        self.player_color = player_color
        self.num_particles = num_particles
        self.walls = []
        for row in range(MAZE_HEIGHT):
            for col in range(MAZE_WIDTH):
                if self.maze[row][col] == "w":
                    self.walls.append((row, col))
        self.rect_walls = [pygame.rect.Rect(
                    (MARGIN + CELL_SIZE) * wall[1] + MARGIN, (MARGIN + CELL_SIZE) * wall[0] + MARGIN, CELL_SIZE,
                    CELL_SIZE
                ) for wall in self.walls]

    def start(self):
        running = True
        particles = ParticleCluster(self.start_coordinates, self.player_color, self.num_particles)

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
            self.WINDOW.fill(Colors.WHITE.value)

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
                        self.WINDOW,
                        color,
                        [(MARGIN + CELL_SIZE) * col + MARGIN, (MARGIN + CELL_SIZE) * row + MARGIN, CELL_SIZE,
                         CELL_SIZE],
                    )

            exit_found_or_error = particles.update(self.maze, self.WINDOW)

            if exit_found_or_error:
                break

            for wall in self.rect_walls:
                already_collided = []
                collisions = wall.collidelistall(particles.collision_rects)
                if collisions:
                    collisionned_particles = [particles.particles[collision] for collision in collisions]
                    for particle in collisionned_particles:
                        if particle not in already_collided:
                            particle.handle_collision(wall)
                            already_collided.append(particle)


            # Update the display
            pygame.display.flip()
            self.clock.tick(60)

        # Quit Pygame
        pygame.quit()
        sys.exit()

