from constants import *
import random


def pixel_to_cell(coordinate):
    return int((coordinate - MARGIN) // (CELL_SIZE + MARGIN))


def cell_to_pixel(cell):
    return int(cell * (CELL_SIZE + MARGIN) + CELL_SIZE // 2)


def generate_noise():
    return random.uniform(-0.1, 0.1)
