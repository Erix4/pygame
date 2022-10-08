import random
import pygame
import numpy as np

#written without oop

WIDTH, HEIGHT = 900, 500
MIN_SIZE = 6

def pretty_print(td_array):
    for row in td_array:
        print(row)

def get_options(pos, maze_path):
    options = []
    if(pos[0] + 1 < len(maze_path) and maze_path[pos[0] + 1][pos[1]]):
        options.append(0)
    if(pos[0] - 1 > 0 and maze_path[pos[0] - 1][pos[1]]):
        options.append(2)
    if(pos[1] + 1 < len(maze_path) and maze_path[pos[0]][pos[1] + 1]):
        options.append(1)
    if(pos[1] - 1 > 0 and maze_path[pos[0] - 1][pos[1]]):
        options.append(3)
    

def gen_maze(size):
    maze_walls = np.ones((size * 2 + 1, size), dtype=int).tolist()
    maze_path = np.zeros((size, size), dtype=int).tolist()
    #
    pos = [0, 0]
    maze_path[0][0] = 1
    maze_walls[0][0] = 0
    #
    for x in range(size):
        maze_walls[size * 2][x] = 0
    #
    pathing = True
    while(pathing):
        options = get_options(pos, maze_path)
        move = options[random.randint(0, len(options) - 1)]
    #
    pretty_print(maze_path)
    pretty_print(maze_walls)

def main():
    pygame.init()
    #
    mode = 0 #0 = menu screen, 1 = run maze, 2 = win
    level = 0
    #
    maze_walls = gen_maze(MIN_SIZE)
    #
    running = True
    while running:
        match mode:
            case 0:
                pass
            case 1:
                pass
            case 2:
                pass
        running = False    
    #
    pygame.quit()

if __name__ == "__main__":
    main()