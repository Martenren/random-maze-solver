import sys
from particle import ParticleCluster
from utils import *
import multiprocessing
import pygame
import os
import maze_creation


class Game:
    def __init__(self, WINDOW, player_color, num_particles, maze_algorithm):
        pygame.init()
        self.WINDOW = WINDOW
        self.maze_algorithm = maze_algorithm
        self.player_color = player_color
        self.num_particles = num_particles
        self.maze = []
        self.start_coordinates = 0
        self.end_coordinates = 0
        self.clock = pygame.time.Clock()
        self.walls = []
        self.rect_walls = []
        self.particles = []
        self.cell_colors = []
        self.rects = []

    def update_walls(self):
        for row in range(MAZE_HEIGHT):
            for col in range(MAZE_WIDTH):
                if self.maze[row][col] == "w":
                    self.walls.append((row, col))
        self.rect_walls = [pygame.rect.Rect(
                    (MARGIN + CELL_SIZE) * wall[1] + MARGIN, (MARGIN + CELL_SIZE) * wall[0] + MARGIN, CELL_SIZE,
                    CELL_SIZE
                ) for wall in self.walls]

    def setup_maze(self):
        self.maze, self.start_coordinates, self.end_coordinates, cell_colors, rects = maze_creation.maze_generation(
            self.WINDOW, self.maze_algorithm)

        for row in range(MAZE_HEIGHT):
            for col in range(MAZE_WIDTH):
                if self.maze[row][col] == "w":
                    self.walls.append((row, col))
        self.rect_walls = [pygame.rect.Rect(
                    (MARGIN + CELL_SIZE) * wall[1] + MARGIN, (MARGIN + CELL_SIZE) * wall[0] + MARGIN, CELL_SIZE,
                    CELL_SIZE
                ) for wall in self.walls]

        return cell_colors, rects

    def draw_maze(self, cell_colors, rects):
        # Draw the maze and update the display
        for color, rect in zip(cell_colors, rects):
            pygame.draw.rect(self.WINDOW, color, rect)
        return True

    def start(self):
        running = True
        first_time_setup = True

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
                            self.update_walls()

            self.WINDOW.fill(Colors.WHITE.value)

            if first_time_setup:
                self.cell_colors, self.rects = self.setup_maze()
                self.particles = ParticleCluster(self.start_coordinates, self.player_color, self.num_particles)
                first_time_setup = False

            else:
                self.draw_maze(self.cell_colors, self.rects)

                exit_found_or_error = self.particles.update(self.maze, self.WINDOW)

                if exit_found_or_error:
                    break

                for wall in self.rect_walls:
                    already_collided = []
                    collisions = wall.collidelistall(self.particles.collision_rects)
                    if collisions:
                        collisionned_particles = [self.particles.this[collision] for collision in collisions]
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

