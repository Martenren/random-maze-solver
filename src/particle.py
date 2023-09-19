import pygame
import math
import random
from utils import *


def particle_creation(start_coordinates, width, height, velocity_x, velocity_y, number):
    start_coordinates = (cell_to_pixel(start_coordinates[0]), cell_to_pixel(start_coordinates[1]))
    print(start_coordinates)
    return [Particle(
        (start_coordinates[0] * random.randint(-10, 10)),
        (start_coordinates[1] * random.randint(-10, 10)),
        width,
        height,
        velocity_x + random.random() / 10,
        velocity_y + random.random() / 10,
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
        # Calculate the angle of rotation based on velocity
        angle = math.atan2(self.velocity_y, self.velocity_x) * (180 / math.pi)

        # Rotate the image
        rotated_image = pygame.transform.rotate(self.image, angle)  # Use -angle to match the direction

        # Get the rect of the rotated image
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        # Draw the rotated image on the surface
        surface.blit(rotated_image, rotated_rect.topleft)

    def handle_collision(self, maze, MARGIN, CELL_SIZE, surface, MAZE_WIDTH, MAZE_HEIGHT):
        cell_x = int((self.x - MARGIN) / (CELL_SIZE + MARGIN))
        cell_y = int((self.y - MARGIN) / (CELL_SIZE + MARGIN))

        rect = self.image.get_rect(center=(self.x, self.y))
        pygame.draw.rect(surface, color=[0, 255, 255], rect=rect)

        # Calculate the cell coordinates for the top-left and bottom-right corners of the bounding box
        top_left_cell_x = int((rect.left - MARGIN) / (CELL_SIZE + MARGIN))
        top_left_cell_y = int((rect.top - MARGIN) / (CELL_SIZE + MARGIN))
        bottom_right_cell_x = int((rect.right - MARGIN) / (CELL_SIZE + MARGIN))
        bottom_right_cell_y = int((rect.bottom - MARGIN) / (CELL_SIZE + MARGIN))

        # Determine the direction of the arrow's movement
        dx = self.velocity_x
        dy = self.velocity_y

        # Iterate through cells within the bounding box
        for cell_x in range(top_left_cell_x, bottom_right_cell_x + 1):
            for cell_y in range(top_left_cell_y, bottom_right_cell_y + 1):
                if 0 <= cell_x < MAZE_WIDTH and 0 <= cell_y < MAZE_HEIGHT:
                    if maze[cell_y][cell_x] == 'w':
                        # Check for collision with the cell's rectangle
                        cell_rect = pygame.Rect(
                            cell_x * (CELL_SIZE + MARGIN) + MARGIN,
                            cell_y * (CELL_SIZE + MARGIN) + MARGIN,
                            CELL_SIZE,
                            CELL_SIZE
                        )
                        if rect.colliderect(cell_rect):
                            pygame.draw.rect(surface, color=[255, 0, 0], rect=cell_rect)
                            # Handle collision by inverting the appropriate velocity component
                            if dx > 0 and dy > 0:   # Arrow moving down and right
                                if rect.bottom - cell_rect.top < rect.right - cell_rect.left:
                                    self.invert_velocity_y()
                                else:
                                    self.invert_velocity_x()
                                # exit()
                            elif dx > 0 > dy:  # Arrow moving up and right
                                if cell_rect.bottom - rect.top < rect.right - cell_rect.left:
                                    self.invert_velocity_y()
                                else:
                                    self.invert_velocity_x()
                            elif dx < 0 < dy:  # Arrow moving down and left
                                if rect.bottom - cell_rect.top < cell_rect.right - rect.left:
                                    self.invert_velocity_y()
                                else:
                                    self.invert_velocity_x()
                            elif dx < 0 and dy < 0:  # Arrow moving up and left
                                if cell_rect.bottom - rect.top < cell_rect.right - rect.left:
                                    self.invert_velocity_y()
                                else:
                                    self.invert_velocity_x()
                            elif dx == 0 and dy > 0:  # Arrow moving down
                                self.invert_velocity_y()
                            elif dx == 0 and dy < 0:  # Arrow moving up
                                self.invert_velocity_y()
                            elif dx > 0 and dy == 0:  # Arrow moving right
                                self.invert_velocity_x()
                            elif dx < 0 and dy == 0:  # Arrow moving left
                                self.invert_velocity_x()



