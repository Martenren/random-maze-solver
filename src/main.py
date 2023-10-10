import random
from game import Game
from joblib import Parallel, delayed
import pygame
from constants import *
import os
import time


def game_loop(desired_position,  color, maze_algorithm, seed, random_mazes):
    if not random_mazes:
        random.seed(seed)
    os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(*desired_position)
    WINDOW = pygame.display.set_mode(WINDOW_SIZE)

    game = Game(WINDOW, color, 100, maze_algorithm)
    game.start()


def display_timer(window, timer_font, shared_timer):
    while True:
        window.fill((255, 255, 255))  # Clear the window
        timer_text = timer_font.render(f"Time: {int(shared_timer[0])} seconds", True, (0, 0, 0))  # Render the timer text
        text_rect = timer_text.get_rect(center=(window.get_width() // 2, window.get_height() // 2))
        window.blit(timer_text, text_rect)  # Blit the text onto the window
        pygame.display.flip()


if __name__ == "__main__":
    nb_games = int(input("Enter number of simultaneous games:"))

    # for color in Colors:
    #     with codecs.open('../assets/particle.svg', encoding='utf-8', errors='ignore') as f:
    #         particle_svg = f.read()
    #         particle_svg = particle_svg.replace('#666666', color.value)  # Replace the color
    #
    #     with open(f'../assets/particles/particle_{color.name.lower()}.svg', 'w', encoding='utf-8') as f:
    #         f.write(particle_svg)

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

    maze_algorithm = input(
        "Enter maze generation algorithm (prim, kruskal, recursive_backtracking, wilson, aldous_broder):")

    random_mazes = True if input("Random mazes? (y/n):") == "y" else False

    seed = random.uniform(0, time.time())

    # Start the game loops in parallel
    Parallel(n_jobs=num_jobs)(
        delayed(game_loop)(desired_position, color, maze_algorithm, seed, random_mazes)
        for i, color, desired_position in zip(range(num_jobs), sub_colors, desired_positions))


