import pygame
import sys
from constants import *

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT = pygame.font.Font(None, 20)

# Maze generation algorithms
MAZE_ALGORITHMS = ["Prim", "Kruskal", "Recursive backtracking", "Wilson", "Aldous-broder"]

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Main Menu")


# Function to display text and get user input
def draw_text(text, x, y):
    text_surface = FONT.render(text, True, Colors.BLACK.value)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


def draw_input_box(input_box, text):
    draw_text(text, input_box.midleft[0] + 10, input_box.midleft[1] - 5)
    pygame.draw.rect(screen, Colors.BLACK.value, input_box, 2)


def draw_checkbox(prompt, x, y, selected):
    checkbox_rect = pygame.Rect(x, y, 20, 20)
    pygame.draw.rect(screen, Colors.BLACK.value, checkbox_rect, 2)
    if selected:
        pygame.draw.line(screen, Colors.BLACK.value, (x, y), (x + 20, y + 20), 2)
        pygame.draw.line(screen, Colors.BLACK.value, (x + 20, y), (x, y + 20), 2)
    draw_text(prompt, x + 30, y)
    return checkbox_rect


def draw_button(prompt, rect):
    pygame.draw.rect(screen, Colors.GREEN.value, rect)
    draw_text(prompt, rect.midleft[0] + 10, rect.midleft[1] - 5)


def reformat_selected_algorithm(selected_algorithm):
    if selected_algorithm == "Recursive backtracking":
        return "recursive_backtracking"
    elif selected_algorithm == "Aldous-broder":
        return "aldous_broder"
    else:
        return selected_algorithm.lower()


def main_menu():
    prompts = ["Enter number of simultaneous games:",
               "Select maze generation algorithm:",
               "Random mazes?:"]

    questions = [(100, 100), (100, 200), (100, 460)]

    input_box = pygame.Rect(370, 90, 270, 32)

    selected_algorithm_index = 0  # Initial selection
    selected_algorithm = "Prim"
    selected_randomisation_option = 0  # Initial selection
    algorithm_checkboxes_rects = []
    maze_randomisation_checkboxes_rects = []
    number_of_games = 'Number between 0 and number of cores'
    active_input = -1

    continue_rect = pygame.Rect(650, 500, 100, 50)
    running = True

    while running:
        screen.fill(Colors.WHITE.value)

        for i, algorithm in enumerate(MAZE_ALGORITHMS):
            algorithm_checkboxes_rects.append(draw_checkbox(algorithm, 370, 200 + i * 40, i == selected_algorithm_index))

        for i in range(len(questions)):
            draw_text(prompts[i], questions[i][0], questions[i][1])

        draw_input_box(input_box, number_of_games)

        draw_button("continue", continue_rect)

        for i, choice in enumerate(["Yes", "No"]):
            maze_randomisation_checkboxes_rects.append(draw_checkbox(choice, 370, 460 + i * 40, selected_randomisation_option == i))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle maze generation algorithm checkboxes
                for checkbox_rect in algorithm_checkboxes_rects:
                    if checkbox_rect.collidepoint(event.pos):
                        selected_algorithm_index = algorithm_checkboxes_rects.index(checkbox_rect)
                        selected_algorithm = MAZE_ALGORITHMS[selected_algorithm_index]

                for checkbox_rect in maze_randomisation_checkboxes_rects:
                    if checkbox_rect.collidepoint(event.pos):
                        selected_randomisation_option = maze_randomisation_checkboxes_rects.index(checkbox_rect)

                if input_box.collidepoint(event.pos):
                    active_input = 0
                    number_of_games = ''
                else:
                    active_input = -1

                if continue_rect.collidepoint(event.pos):
                    selected_randomisation_option = True if selected_randomisation_option == 0 else False
                    selected_algorithm = reformat_selected_algorithm(selected_algorithm)
                    pygame.quit()
                    return int(number_of_games), selected_algorithm, selected_randomisation_option

            if event.type == pygame.KEYDOWN:
                if active_input == 0:  # Handle number of games input
                    if event.key == pygame.K_RETURN:
                        active_input = -1  # No input selected
                    elif event.key == pygame.K_BACKSPACE:
                        number_of_games = number_of_games[:-1]
                    else:
                        number_of_games += event.unicode

        pygame.display.flip()