import pygame
import math
import random
from utils import *
import time
from constants import *


def particle_creation(start_coordinates, color, number):
    start_coordinates = (cell_to_pixel(start_coordinates[1]), cell_to_pixel(start_coordinates[0]))
    return [Particle(
        start_coordinates[0],
        start_coordinates[1],
        WINDOW_WIDTH // 30,
        WINDOW_HEIGHT // 30,
        random.uniform(-1, 1),
        random.uniform(-1, 1),
        color
    ) for _ in range(number)]


class ParticleCluster:
    def __init__(self, start_coordinates, color, num_particles):
        self.particles = particle_creation(start_coordinates, color, num_particles)
        self.collision_rects = [particle.get_collision_rect() for particle in self.particles]

    def update(self, maze, WINDOW):
        for particle in self.particles:
            cell_x = pixel_to_cell(particle.x)
            cell_y = pixel_to_cell(particle.y)
            try:
                if maze[cell_y][cell_x] == "e":
                    print("Exit found by a particle")
                    print(cell_x, cell_y)
                    print(maze[cell_y][cell_x])
                    return True
            except IndexError:
                print("IndexError")
                print(cell_x, cell_y)
                return True

            particle.move_vertical()
            particle.move_horizontal()
            # particle.handle_collision(maze, MARGIN, CELL_SIZE, WINDOW, MAZE_WIDTH, MAZE_HEIGHT)
            particle.update_rect(particle.x, particle.y, WINDOW)
            particle.draw(WINDOW)
            self.collision_rects = [particle.get_collision_rect() for particle in self.particles]


class Particle:
    def __init__(self, x, y, width, height, vel_x, vel_y, color):
        original_image = pygame.image.load(f'../assets/particles/particle_{color}.svg')

        self.image = pygame.transform.scale(original_image, (width, height))
        self.x = x
        self.y = y

        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.width = width
        self.height = height

        self.velocity_x = vel_x
        self.velocity_y = vel_y

        self.collided_x = False
        self.collided_y = False

    def update_rect(self, x, y, surface):
        self.rect = self.image.get_rect(center=(x, y))
        # pygame.draw.rect(surface, color=Colors.PURPLE.value, rect=self.rect)

    def get_collision_rect(self):
        return self.rect

    def change_velocity_x(self, vel):
        self.velocity_x = vel

    def change_velocity_y(self, vel):
        self.velocity_y = vel

    def invert_velocity_x(self):
        self.velocity_x *= -1

    def invert_velocity_y(self,):
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

    def handle_collision(self, wall):

        collision_box_particle = self.get_collision_rect()

        buffer = 1

        if 0 - buffer <= wall.top - collision_box_particle.bottom <= 0 + buffer:
            # print("bottom collision")
            if self.velocity_y > 0:
                self.invert_velocity_y()
            self.y = wall.top - self.height / 2

        elif 0 - buffer <= wall.bottom - collision_box_particle.top <= 0 + buffer:
            # print("top collision")
            if self.velocity_y < 0:
                self.invert_velocity_y()
            self.y = wall.bottom + self.height / 2

        elif 0 - buffer <= wall.left - collision_box_particle.right <= 0 + buffer:
            # print("right collision")
            if self.velocity_x > 0:
                self.invert_velocity_x()
            self.x = wall.left - self.width / 2

        elif 0 - buffer <= wall.right - collision_box_particle.left <= 0 + buffer:
            # print("left collision")
            if self.velocity_x < 0:
                self.invert_velocity_x()
            self.x = wall.right + self.width / 2

