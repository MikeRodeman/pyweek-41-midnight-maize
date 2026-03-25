import pygame
from constants import *

class Maze:
    def __init__(self):
        # The maze is described with a 2D list of integers between 0 and 15.
        # The integers represent the walls of each cell in the grid, like
        # how Linux file permission numbers work. It's called a 4-bit bitmask.
        #
        # 1 (0001) = North, 2 (0010) = East, 4 (0100) = South, 8 (1000) = West.
        self.grid = [[15 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    def draw(self, surface):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(surface, (40, 40, 40), rect, 1)