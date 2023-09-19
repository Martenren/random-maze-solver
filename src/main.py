import maze_creation as mc
from game import Game


if __name__ == "__main__":
    maze, start_coordinates, end_coordinates = mc.maze_generation()
    game = Game(maze, start_coordinates, end_coordinates)
    game.start()
