import random
from game import Game
from joblib import Parallel, delayed
from main_menu import main_menu
from constants import *
import os
import time
import pygame


def game_loop(desired_position, color, maze_algorithm, seed, random_mazes):
    if not random_mazes:
        random.seed(seed)
    os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(*desired_position)
    WINDOW = pygame.display.set_mode(WINDOW_SIZE)

    game = Game(WINDOW, color, 100, maze_algorithm)
    game.start()


if __name__ == "__main__":
    # nb_games = int(input("Enter number of simultaneous games:"))
    # maze_algorithm = input(
    #     "Enter maze generation algorithm (prim, kruskal, recursive_backtracking, wilson, aldous_broder):")
    # random_mazes = True if input("Random mazes? (y/n):") == "y" else False

    nb_games, maze_algorithm, random_mazes = main_menu()

    # Calculate the screen resolution
    screen_width, screen_height = 1440, 720

    # Define the number of rows and columns for your grid
    num_rows, num_cols = 2, 4

    # Calculate the spacing between windows
    horizontal_spacing = (screen_width - (num_cols * WINDOW_SIZE[0])) // (num_cols + 1)
    vertical_spacing = (screen_height - (num_rows * WINDOW_SIZE[1])) // (num_rows + 1) + 50

    # Create a list to store the Pygame windows
    desired_positions = []

    for row in range(num_rows):
        for col in range(num_cols):
            x = (col * WINDOW_SIZE[0]) + ((col + 1) * horizontal_spacing)
            y = (row * WINDOW_SIZE[1]) + ((row + 1) * vertical_spacing)

            desired_positions.append((x, y))

    colors = [color.name.lower() for color in Colors if color.name.lower() not in ['white', 'black', 'green', 'red']]
    sub_colors = random.sample(colors, k=nb_games)
    num_jobs = nb_games  # Number of parallel jobs

    seed = random.uniform(0, time.time())

    # Start the game loops in parallel
    Parallel(n_jobs=num_jobs)(
        delayed(game_loop)(desired_position, color, maze_algorithm, seed, random_mazes)
        for i, color, desired_position in zip(range(num_jobs), sub_colors, desired_positions))
