import pygame
import math
import random
from utils import *
from constants import *


def particle_creation(start_coordinates, width, height, velocity_x, velocity_y, number):
    start_coordinates = (cell_to_pixel(start_coordinates[1]), cell_to_pixel(start_coordinates[0]))
    return [Particle(
        (start_coordinates[0] + random.randint(-10, 10)),
        (start_coordinates[1] + random.randint(-10, 10)),
        width,
        height,
        velocity_x,
        velocity_y,
        # velocity_x + random.randint(-90, 90) / 1000,
        # velocity_y + random.randint(-90, 90) / 1000,
    ) for _ in range(number)]


class Particle:
    def __init__(self, x, y, width, height, vel_x, vel_y):
        original_image = pygame.image.load('../assets/particle.svg')
        self.image = pygame.transform.scale(original_image, (width, height))
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.velocity_x = vel_x
        self.velocity_y = vel_y

        self.collided_x = False
        self.collided_y = False

    def change_velocity_x(self, vel):
        self.velocity_x = vel

    def change_velocity_y(self, vel):
        self.velocity_y = vel

    def invert_velocity_x(self):
        self.velocity_x *= -1

    def invert_velocity_y(self):
        self.velocity_y *= -1

    def move_horizontal(self):
        self.x += self.velocity_x

    def move_vertical(self):
        self.y += self.velocity_y

    def draw(self, surface):
        angle = math.atan2(self.velocity_x, self.velocity_y) * (180 / math.pi)

        rotated_image = pygame.transform.rotate(self.image, angle)

        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))

        surface.blit(rotated_image, rotated_rect.topleft)

    def handle_collision(self, maze, MARGIN, CELL_SIZE, surface, MAZE_WIDTH, MAZE_HEIGHT):
        cell_x = pixel_to_cell(self.x)
        cell_y = pixel_to_cell(self.y)

        collision_box_particle = self.image.get_rect(center=(self.x, self.y))
        pygame.draw.rect(surface, color=Colors.CYAN.value, rect=collision_box_particle)

        # Determine the direction of the arrow's movement
        dx = self.velocity_x
        dy = self.velocity_y

        # Get the coordinates of the surrounding cells
        surrounding_cells = [(cell_x + dx, cell_y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (cell_x + dx < MAZE_WIDTH and cell_y + dy < MAZE_HEIGHT)]
        surrounding_cells = [(cell_x, cell_y) for cell_x, cell_y in surrounding_cells if maze[cell_y][cell_x] == 'w']
        surrounding_rects = []

        for x, y in surrounding_cells:
            # Check if the cell coordinates are within the maze boundaries
            if 0 <= x < len(maze[0]) and 0 <= y < len(maze):
                # Calculate the pixel coordinates of the cell
                cell_rect = pygame.Rect(
                    x * (CELL_SIZE + MARGIN) + MARGIN,
                    y * (CELL_SIZE + MARGIN) + MARGIN,
                    CELL_SIZE,
                    CELL_SIZE
                )

                pygame.draw.rect(surface, color=Colors.BLUE.value, rect=cell_rect)
                surrounding_rects.append(cell_rect)

        collision = collision_box_particle.collidelist(surrounding_rects)

        buffer = 2

        if collision != -1:
            collision_rect = surrounding_rects[collision]
            pygame.draw.rect(surface, color=Colors.RED.value, rect=collision_rect)

            if collision_box_particle.top - collision_rect.bottom <= 0 + buffer:
                print("bottom collision")
                self.invert_velocity_y()

            elif collision_rect.top - collision_box_particle.bottom >= 0 + buffer:
                print("top collision")
                self.invert_velocity_y()

            elif collision_rect.left - collision_box_particle.right >= 0 + buffer:
                print("right collision")
                self.invert_velocity_x()

            elif collision_box_particle.left - collision_rect.right <= 0 + buffer:
                print("left collision")
                self.invert_velocity_x()


