import codecs

from constants import *
import random


def pixel_to_cell(coordinate):
    return int((coordinate - MARGIN) // (CELL_SIZE + MARGIN))


def cell_to_pixel(cell):
    return int(cell * (CELL_SIZE + MARGIN) + CELL_SIZE // 2)


def generate_noise():
    return random.uniform(-0.1, 0.1)


def generate_svgs_for_particles_based_on_colors():
    for color in Colors:
        with codecs.open('../assets/particle.svg', encoding='utf-8', errors='ignore') as f:
            particle_svg = f.read()
            particle_svg = particle_svg.replace('#666666', color.value)  # Replace the color

        with open(f'../assets/particles/particle_{color.name.lower()}.svg', 'w', encoding='utf-8') as f:
            f.write(particle_svg)
