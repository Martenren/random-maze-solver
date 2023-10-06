import pygame
import math
import random
from utils import *
import codecs
import os


def particle_creation(start_coordinates, color, number):
    start_coordinates = (cell_to_pixel(start_coordinates[1]), cell_to_pixel(start_coordinates[0]))
    return [Particle(
        (start_coordinates[0] + random.randint(-10, 10)),
        (start_coordinates[1] + random.randint(-10, 10)),
        WINDOW_WIDTH // 30,
        WINDOW_HEIGHT // 30,
        1.0,
        1.0,
        color
    ) for _ in range(number)]


class ParticleCluster:
    def __init__(self, start_coordinates, color, num_particles):
        self.particles = particle_creation(start_coordinates, color, num_particles)

    def update(self, maze, WINDOW):
        for particle in self.particles:
            cell_x = pixel_to_cell(particle.x)
            cell_y = pixel_to_cell(particle.y)
            try:
                if maze[cell_y][cell_x] == "e":
                    print("Exit found by a particle")
                    print(cell_x, cell_y)
                    print(maze[cell_y][cell_x])
                    return False
            except IndexError:
                print("IndexError")
                print(cell_x, cell_y)
                return False

            particle.move_vertical()
            particle.move_horizontal()
            particle.handle_collision(maze, MARGIN, CELL_SIZE, WINDOW, MAZE_WIDTH, MAZE_HEIGHT)
            particle.draw(WINDOW)


class Particle:
    def __init__(self, x, y, width, height, vel_x, vel_y, color):
        original_image = pygame.image.load(f'../assets/particles/particle_{color}.svg')

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

    def invert_velocity_x(self, random_vel=False):
        self.velocity_x *= -1 * (random.randint(90, 110) / 100) if random_vel else -1

    def invert_velocity_y(self, random_vel=False):
        self.velocity_y *= -1 * (random.randint(90, 110) / 100) if random_vel else -1

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
        # pygame.draw.rect(surface, color=Colors.CYAN.value, rect=collision_box_particle)

        # Get the coordinates of the surrounding cells
        surrounding_rects = [pygame.Rect((cell_x + dx) * (CELL_SIZE + MARGIN) + MARGIN, (cell_y + dy) * (CELL_SIZE + MARGIN) + MARGIN, CELL_SIZE, CELL_SIZE) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if
                             0 <= cell_x + dx < MAZE_WIDTH and 0 <= cell_y + dy < MAZE_HEIGHT and maze[cell_y + dy][
                                 cell_x + dx] == 'w']

        # for surrounding_rect in surrounding_rects:
        #     pygame.draw.rect(surface, color=Colors.BLUE.value, rect=surrounding_rect)

        collision = collision_box_particle.collidelist(surrounding_rects)

        buffer = 1

        if collision != -1:
            collision_rect = surrounding_rects[collision]
            # pygame.draw.rect(surface, color=Colors.RED.value, rect=collision_rect)

            if 0 - buffer <= collision_rect.top - collision_box_particle.bottom <= 0 + buffer:
                # print("bottom collision")
                self.invert_velocity_y()
                self.y = collision_rect.top - self.height / 2

            elif 0 - buffer <= collision_rect.bottom - collision_box_particle.top <= 0 + buffer:
                self.invert_velocity_y()
                self.y = collision_rect.bottom + self.height / 2

            elif 0 - buffer <= collision_rect.left - collision_box_particle.right <= 0 + buffer:
                self.invert_velocity_x()
                self.x = collision_rect.left - self.width / 2

            elif 0 - buffer <= collision_rect.right - collision_box_particle.left <= 0 + buffer:
                self.invert_velocity_x()
                self.x = collision_rect.right + self.width / 2