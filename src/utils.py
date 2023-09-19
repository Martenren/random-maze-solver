from constants import *


def pixel_to_cell(coordinate):
    return int((coordinate - MARGIN) // (CELL_SIZE + MARGIN))


def cell_to_pixel(cell):
    return int(cell * (CELL_SIZE + MARGIN) + CELL_SIZE // 2)